"""Inspect an ONNX computation graph.

Usage:
    python inspect_onnx_graph.py tiny_model.onnx
    python inspect_onnx_graph.py tiny_model.onnx --json report.json --dot graph.dot
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import onnx


FUSION_PATTERNS = {
    ("Gemm", "Relu"): "activation fusion candidate",
    ("MatMul", "Add"): "linear fusion candidate",
    ("Add", "Relu"): "bias-add activation fusion candidate",
    ("Conv", "BatchNormalization"): "conv-batchnorm folding candidate",
    ("BatchNormalization", "Relu"): "batchnorm-activation fusion candidate",
}


def tensor_dtype_name(data_type: int) -> str:
    try:
        return onnx.TensorProto.DataType.Name(data_type)
    except ValueError:
        return f"UNKNOWN({data_type})"


def format_shape(value_info: onnx.ValueInfoProto) -> str:
    tensor_type = value_info.type.tensor_type
    if not tensor_type.HasField("shape"):
        return "unknown"

    dims: list[str] = []
    for dim in tensor_type.shape.dim:
        if dim.dim_param:
            dims.append(dim.dim_param)
        elif dim.HasField("dim_value"):
            dims.append(str(dim.dim_value))
        else:
            dims.append("?")
    return "[" + ", ".join(dims) + "]"


def initializer_num_elements(initializer: onnx.TensorProto) -> int:
    if not initializer.dims:
        return 1
    return math.prod(initializer.dims)


def node_display_name(node: onnx.NodeProto, index: int) -> str:
    return node.name or f"node_{index}_{node.op_type}"


def build_graph_indexes(
    graph: onnx.GraphProto,
) -> tuple[dict[str, int], dict[str, str], dict[str, list[str]]]:
    output_to_node_index: dict[str, int] = {}
    tensor_producer: dict[str, str] = {}
    tensor_consumers: dict[str, list[str]] = defaultdict(list)

    for index, node in enumerate(graph.node):
        name = node_display_name(node, index)
        for output in node.output:
            output_to_node_index[output] = index
            tensor_producer[output] = name
        for input_name in node.input:
            if input_name:
                tensor_consumers[input_name].append(name)

    return output_to_node_index, tensor_producer, dict(tensor_consumers)


def summarize_values(values: list[onnx.ValueInfoProto]) -> list[dict[str, str]]:
    return [{"name": value.name, "shape": format_shape(value)} for value in values]


def summarize_initializers(graph: onnx.GraphProto) -> list[dict[str, Any]]:
    result = []
    for initializer in graph.initializer:
        result.append(
            {
                "name": initializer.name,
                "dtype": tensor_dtype_name(initializer.data_type),
                "shape": list(initializer.dims),
                "num_elements": initializer_num_elements(initializer),
            }
        )
    return result


def summarize_nodes(graph: onnx.GraphProto) -> list[dict[str, Any]]:
    result = []
    for index, node in enumerate(graph.node):
        result.append(
            {
                "index": index,
                "name": node_display_name(node, index),
                "op_type": node.op_type,
                "inputs": list(node.input),
                "outputs": list(node.output),
            }
        )
    return result


def find_unused_initializers(
    graph: onnx.GraphProto, tensor_consumers: dict[str, list[str]]
) -> list[str]:
    return [
        initializer.name
        for initializer in graph.initializer
        if not tensor_consumers.get(initializer.name)
    ]


def find_unused_node_outputs(
    graph: onnx.GraphProto, tensor_consumers: dict[str, list[str]]
) -> list[str]:
    graph_outputs = {value.name for value in graph.output}
    unused_outputs: list[str] = []

    for node in graph.node:
        for output in node.output:
            if output not in graph_outputs and not tensor_consumers.get(output):
                unused_outputs.append(output)

    return unused_outputs


def find_fusion_candidates(
    graph: onnx.GraphProto,
    output_to_node_index: dict[str, int],
    tensor_consumers: dict[str, list[str]],
) -> list[dict[str, Any]]:
    node_name_to_index = {
        node_display_name(node, index): index for index, node in enumerate(graph.node)
    }
    candidates: list[dict[str, Any]] = []

    for producer_index, producer in enumerate(graph.node):
        producer_name = node_display_name(producer, producer_index)
        for output in producer.output:
            consumers = tensor_consumers.get(output, [])
            if len(consumers) != 1:
                continue

            consumer_name = consumers[0]
            consumer_index = node_name_to_index.get(consumer_name)
            if consumer_index is None:
                continue

            consumer = graph.node[consumer_index]
            pattern = (producer.op_type, consumer.op_type)
            reason = FUSION_PATTERNS.get(pattern)
            if not reason:
                continue

            candidates.append(
                {
                    "producer_index": producer_index,
                    "producer": producer_name,
                    "producer_op": producer.op_type,
                    "consumer_index": consumer_index,
                    "consumer": consumer_name,
                    "consumer_op": consumer.op_type,
                    "tensor": output,
                    "reason": reason,
                }
            )

    return candidates


def build_report(model_path: Path, model: onnx.ModelProto) -> dict[str, Any]:
    graph = model.graph
    output_to_node_index, tensor_producer, tensor_consumers = build_graph_indexes(graph)
    initializers = summarize_initializers(graph)
    nodes = summarize_nodes(graph)
    op_counts = Counter(node["op_type"] for node in nodes)

    return {
        "model": str(model_path),
        "graph_name": graph.name or "",
        "opsets": [
            {"domain": opset.domain, "version": opset.version}
            for opset in model.opset_import
        ],
        "inputs": summarize_values(list(graph.input)),
        "outputs": summarize_values(list(graph.output)),
        "initializers": initializers,
        "parameter_summary": {
            "total_initializers": len(initializers),
            "total_parameters": sum(item["num_elements"] for item in initializers),
        },
        "operator_summary": dict(sorted(op_counts.items())),
        "nodes": nodes,
        "tensor_dependencies": {
            tensor: {
                "producer": producer,
                "consumers": tensor_consumers.get(tensor, []),
            }
            for tensor, producer in tensor_producer.items()
        },
        "unused_initializers": find_unused_initializers(graph, tensor_consumers),
        "unused_node_outputs": find_unused_node_outputs(graph, tensor_consumers),
        "fusion_candidates": find_fusion_candidates(
            graph, output_to_node_index, tensor_consumers
        ),
    }


def print_list_section(title: str, rows: list[str]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if not rows:
        print("(none)")
        return
    for row in rows:
        print(row)


def print_report(report: dict[str, Any]) -> None:
    print(f"Model: {report['model']}")
    print(f"Graph name: {report['graph_name'] or '(empty)'}")
    print(
        "Opset imports: "
        + ", ".join(
            f"{item['domain'] or 'ai.onnx'}:{item['version']}"
            for item in report["opsets"]
        )
    )

    print_list_section(
        "Graph Inputs",
        [f"{item['name']}: shape={item['shape']}" for item in report["inputs"]],
    )
    print_list_section(
        "Graph Outputs",
        [f"{item['name']}: shape={item['shape']}" for item in report["outputs"]],
    )

    print("\nOperator Summary")
    print("----------------")
    if report["operator_summary"]:
        for op_type, count in report["operator_summary"].items():
            print(f"{op_type}: {count}")
    else:
        print("(none)")

    params = report["parameter_summary"]
    print("\nParameter Summary")
    print("-----------------")
    print(f"total initializers: {params['total_initializers']}")
    print(f"total parameters : {params['total_parameters']}")

    print_list_section(
        "Initializers",
        [
            f"{item['name']}: dtype={item['dtype']}, "
            f"shape={'x'.join(map(str, item['shape'])) or 'scalar'}, "
            f"params={item['num_elements']}"
            for item in report["initializers"]
        ],
    )

    print("\nNodes")
    print("-----")
    if not report["nodes"]:
        print("(none)")
    for node in report["nodes"]:
        inputs = ", ".join(node["inputs"]) if node["inputs"] else "(none)"
        outputs = ", ".join(node["outputs"]) if node["outputs"] else "(none)"
        print(f"[{node['index']}] {node['name']}: op={node['op_type']}")
        print(f"    inputs : {inputs}")
        print(f"    outputs: {outputs}")

    print_list_section(
        "Tensor Dependencies",
        [
            f"{tensor}: produced by {info['producer']}; consumed by "
            f"{', '.join(info['consumers']) if info['consumers'] else '(graph output or unused)'}"
            for tensor, info in report["tensor_dependencies"].items()
        ],
    )

    print_list_section("Unused Initializers", report["unused_initializers"])
    print_list_section("Unused Node Outputs", report["unused_node_outputs"])

    print_list_section(
        "Fusion Candidates",
        [
            f"[{item['producer_index']} -> {item['consumer_index']}] "
            f"{item['producer']} ({item['producer_op']}) -> "
            f"{item['consumer']} ({item['consumer_op']}): {item['reason']}"
            for item in report["fusion_candidates"]
        ],
    )


def dot_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def write_dot(report: dict[str, Any], output_path: Path) -> None:
    lines = [
        "digraph onnx_graph {",
        "  rankdir=LR;",
        '  node [shape=box, style="rounded,filled", fillcolor="#eef5ff"];',
    ]

    for node in report["nodes"]:
        label = f"{node['index']}: {node['name']}\\n{node['op_type']}"
        lines.append(f'  n{node["index"]} [label="{dot_escape(label)}"];')

    output_to_node = {
        output: node["index"] for node in report["nodes"] for output in node["outputs"]
    }

    for consumer in report["nodes"]:
        for input_name in consumer["inputs"]:
            producer_index = output_to_node.get(input_name)
            if producer_index is None:
                continue
            lines.append(
                f'  n{producer_index} -> n{consumer["index"]} '
                f'[label="{dot_escape(input_name)}"];'
            )

    lines.append("}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(report: dict[str, Any], output_path: Path) -> None:
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def inspect_model(model_path: Path, json_path: Path | None, dot_path: Path | None) -> None:
    model = onnx.load(model_path)
    onnx.checker.check_model(model)

    report = build_report(model_path, model)
    print_report(report)

    if json_path:
        write_json(report, json_path)
        print(f"\nWrote JSON report: {json_path}")

    if dot_path:
        write_dot(report, dot_path)
        print(f"Wrote DOT graph: {dot_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect an ONNX graph.")
    parser.add_argument(
        "model",
        nargs="?",
        default="tiny_model.onnx",
        help="Path to an ONNX model. Default: tiny_model.onnx",
    )
    parser.add_argument("--json", type=Path, help="Write a JSON graph report.")
    parser.add_argument("--dot", type=Path, help="Write a Graphviz DOT graph.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_path = Path(args.model)
    if not model_path.exists():
        raise FileNotFoundError(
            f"ONNX model not found: {model_path}. Run export_tiny_model.py first."
        )
    inspect_model(model_path, args.json, args.dot)


if __name__ == "__main__":
    main()

