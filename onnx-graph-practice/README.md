# ONNX Graph Practice

This directory contains a tiny ONNX workflow:

1. Build a small PyTorch model.
2. Export the model to ONNX.
3. Inspect the ONNX computation graph.

The goal is to understand how an AI model can be represented as a graph of
operators, tensors, inputs, outputs, and parameters.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Export Tiny Model

```bash
python export_tiny_model.py
```

This creates:

```text
tiny_model.onnx
```

## Inspect ONNX Graph

```bash
python inspect_onnx_graph.py tiny_model.onnx
```

The script prints:

- graph inputs
- graph outputs
- initializers
- operator nodes
- producer-consumer dependencies between tensors and nodes

## Why This Matters

In AI compiler and model deployment workflows, the model is often transformed
from a framework-level representation into an intermediate graph format such as
ONNX. Graph-level optimization can then analyze operators and tensor
dependencies.

Common optimization ideas include:

- constant folding
- operator fusion, such as MatMul + Add
- removing unused nodes
- backend-specific lowering

