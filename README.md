# Compiler AI Practice

This repository records a small, runnable learning practice around compiler
basics, LLVM IR, classic optimization ideas, and ONNX computation graph
inspection.

The project is designed to match the compiler/programming-language and AI
compiler learning experience described in my resume. It is not an industrial
compiler implementation. Instead, it focuses on concrete, verifiable examples:
handwritten LLVM IR, optimization notes, and simple ONNX graph export and
inspection scripts.

## Project Structure

```text
.
├── README.md
├── llvm-ir-practice/
│   ├── 01_arithmetic.ll
│   ├── 02_if_else.ll
│   ├── 03_loop.ll
│   ├── 04_function_call.ll
│   └── README.md
├── optimization-notes/
│   ├── constant_folding.md
│   ├── dead_code_elimination.md
│   └── common_subexpression.md
├── onnx-graph-practice/
│   ├── export_tiny_model.py
│   ├── inspect_onnx_graph.py
│   ├── requirements.txt
│   └── README.md
└── docs/
    ├── compiler_learning_notes.md
    └── resume_mapping.md
```

## What This Repository Demonstrates

### 1. LLVM IR Practice

The `llvm-ir-practice/` directory contains handwritten LLVM IR examples for:

- arithmetic operations
- conditional branches
- loop control flow
- function calls

These examples help connect high-level programming constructs with lower-level
IR representation.

### 2. Compiler Optimization Notes

The `optimization-notes/` directory explains several basic compiler
optimization ideas:

- constant folding
- dead code elimination
- common subexpression elimination

Each note includes the motivation, a simple before/after example, and how the
idea appears in an IR-level compiler pipeline.

### 3. ONNX Graph Practice

The `onnx-graph-practice/` directory contains Python scripts for:

- exporting a tiny PyTorch model to ONNX
- loading an ONNX model
- inspecting operators, graph inputs, graph outputs, initializers, and node
  dependencies

This part connects AI model deployment with computation graph IR concepts.

## Quick Start

### Run LLVM IR Examples

If LLVM is installed:

```bash
cd llvm-ir-practice
lli 01_arithmetic.ll
lli 02_if_else.ll
lli 03_loop.ll
lli 04_function_call.ll
```

Or compile with `clang`:

```bash
clang 01_arithmetic.ll -o arithmetic
./arithmetic
```

### Run ONNX Graph Practice

```bash
cd onnx-graph-practice
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python export_tiny_model.py
python inspect_onnx_graph.py tiny_model.onnx
```

## Learning Notes

See [docs/compiler_learning_notes.md](docs/compiler_learning_notes.md) for a
compact summary of compiler pipeline concepts, including lexical analysis,
syntax analysis, AST, IR, control flow graph, optimization passes, and code
generation.

See [docs/resume_mapping.md](docs/resume_mapping.md) for the mapping between
this repository and the project descriptions in the resume.

