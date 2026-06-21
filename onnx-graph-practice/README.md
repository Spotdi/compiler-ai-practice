# ONNX Graph Practice

This directory contains a small ONNX model export workflow and a practical
graph inspection tool.

The goal is to make AI model graphs easier to inspect before deployment. The
inspector can summarize operators, parameters, tensor dependencies, unused graph
artifacts, and simple fusion opportunities.

## Install

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r onnx-graph-practice/requirements.txt
```

`onnxscript` is included for compatibility with newer PyTorch ONNX export
paths.

## Export Tiny Model

```bash
cd onnx-graph-practice
python export_tiny_model.py
```

This creates:

```text
tiny_model.onnx
```

Depending on the PyTorch exporter version, an external data file such as
`tiny_model.onnx.data` may also be generated. It is ignored by Git.

## Inspect ONNX Graph

```bash
python inspect_onnx_graph.py tiny_model.onnx
```

The script prints:

- graph inputs and outputs
- operator counts
- initializer shapes and total parameter count
- every node's inputs and outputs
- producer-consumer tensor dependencies
- unused initializers
- unused node outputs
- simple fusion candidates

## Generate Reports

Write a JSON report:

```bash
python inspect_onnx_graph.py tiny_model.onnx --json graph_report.json
```

Write a Graphviz DOT graph:

```bash
python inspect_onnx_graph.py tiny_model.onnx --dot graph.dot
```

Generate both:

```bash
python inspect_onnx_graph.py tiny_model.onnx \
  --json graph_report.json \
  --dot graph.dot
```

If Graphviz is installed, render the DOT file:

```bash
dot -Tpng graph.dot -o graph.png
```

## Practical Questions It Helps Answer

- Which operators must my inference backend support?
- How many parameters does the model contain?
- Which node produced a tensor, and which nodes consume it?
- Are there unused initializers or dead graph outputs?
- Are there simple patterns that may be fused by a backend?
- Can I generate a graph visualization for debugging or documentation?

## Why This Matters

In AI compiler and model deployment workflows, the model is often transformed
from a framework-level representation into an intermediate graph format such as
ONNX. Graph-level analysis can then support optimization, backend selection,
debugging, and deployment preparation.
