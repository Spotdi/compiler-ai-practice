"""Inspect an ONNX computation graph.

Usage:
    python inspect_onnx_graph.py tiny_model.onnx
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import onnx


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


def print_value_infos(title: str, values: list[onnx.ValueInfoProto]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if not values:
        print("(none)")
        return

    for value in values:
        print(f"{value.name}: shape={format_shape(value)}")


def print_initializers(graph: onnx.GraphProto) -> None:
    print("\nInitializers")
    print("------------")
    if not graph.initializer:
        print("(none)")
        return

    for initializer in graph.initializer:
        dims = "x".join(str(dim) for dim in initializer.dims)
        print(f"{initializer.name}: dtype={initializer.data_type}, shape={dims}")


def print_nodes(graph: onnx.GraphProto) -> None:
    print("\nNodes")
    print("-----")
    if not graph.node:
        print("(none)")
        return

    for index, node in enumerate(graph.node):
        name = node.name or f"<unnamed_{index}>"
        inputs = ", ".join(node.input) if node.input else "(none)"
        outputs = ", ".join(node.output) if node.output else "(none)"
        print(f"[{index}] {name}: op={node.op_type}")
        print(f"    inputs : {inputs}")
        print(f"    outputs: {outputs}")


def print_dependencies(graph: onnx.GraphProto) -> None:
    tensor_producer: dict[str, str] = {}
    tensor_consumers: dict[str, list[str]] = defaultdict(list)

    for index, node in enumerate(graph.node):
        node_name = node.name or f"<unnamed_{index}:{node.op_type}>"
        for output in node.output:
            tensor_producer[output] = node_name
        for input_name in node.input:
            tensor_consumers[input_name].append(node_name)

    print("\nTensor Dependencies")
    print("-------------------")
    if not tensor_producer:
        print("(none)")
        return

    for tensor, producer in tensor_producer.items():
        consumers = tensor_consumers.get(tensor, [])
        consumer_text = ", ".join(consumers) if consumers else "(graph output or unused)"
        print(f"{tensor}: produced by {producer}; consumed by {consumer_text}")


def inspect_model(model_path: Path) -> None:
    model = onnx.load(model_path)
    onnx.checker.check_model(model)

    graph = model.graph
    print(f"Model: {model_path}")
    print(f"Graph name: {graph.name or '(empty)'}")
    print(f"Opset imports: {[opset.version for opset in model.opset_import]}")

    print_value_infos("Graph Inputs", list(graph.input))
    print_value_infos("Graph Outputs", list(graph.output))
    print_initializers(graph)
    print_nodes(graph)
    print_dependencies(graph)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect an ONNX graph.")
    parser.add_argument(
        "model",
        nargs="?",
        default="tiny_model.onnx",
        help="Path to an ONNX model. Default: tiny_model.onnx",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_path = Path(args.model)
    if not model_path.exists():
        raise FileNotFoundError(
            f"ONNX model not found: {model_path}. Run export_tiny_model.py first."
        )
    inspect_model(model_path)


if __name__ == "__main__":
    main()

