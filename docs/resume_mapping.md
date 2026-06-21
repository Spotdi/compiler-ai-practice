# Resume Mapping

This document maps the repository content to the compiler and AI compiler
practice described in the resume.

## Compiler Basics and LLVM IR Practice

Resume description:

> Systematically learned the basic compiler process, including frontend,
> intermediate representation, backend, lexical analysis, syntax analysis, AST,
> symbol table, control flow graph, IR optimization, and code generation.

Repository evidence:

- `docs/compiler_learning_notes.md`
  - summarizes the compiler pipeline
  - explains lexer, parser, AST, symbol table, IR, CFG, optimization, and code
    generation
- `llvm-ir-practice/`
  - gives concrete LLVM IR examples for common programming constructs

## LLVM IR Experiments

Resume description:

> Read and wrote simple LLVM IR examples, including variable operations,
> conditional branches, loop control, and function calls, and verified them
> with lli / clang.

Repository evidence:

- `llvm-ir-practice/01_arithmetic.ll`
  - integer arithmetic operations
- `llvm-ir-practice/02_if_else.ll`
  - conditional branch and basic blocks
- `llvm-ir-practice/03_loop.ll`
  - loop control flow and `phi` nodes
- `llvm-ir-practice/04_function_call.ll`
  - function definition and call instruction
- `llvm-ir-practice/README.md`
  - explains how to run the examples with `lli` or compile with `clang`

## Optimization Pass Understanding

Resume description:

> Learned basic optimization ideas such as constant folding, common
> subexpression elimination, and dead code elimination. Analyzed IR changes
> before and after optimization.

Repository evidence:

- `optimization-notes/constant_folding.md`
  - explains compile-time evaluation of constant expressions
- `optimization-notes/dead_code_elimination.md`
  - explains liveness and side-effect checks
- `optimization-notes/common_subexpression.md`
  - explains expression reuse, local CSE, and global CSE

## AI Model Deployment and Computation Graph Optimization

Resume description:

> Learned the PyTorch / ONNX model export and inference deployment process, and
> understood the relationship between operators, computation graphs,
> intermediate representations, and backend execution.

Repository evidence:

- `onnx-graph-practice/export_tiny_model.py`
  - exports a small PyTorch model to ONNX
- `onnx-graph-practice/inspect_onnx_graph.py`
  - loads and checks an ONNX model
  - prints graph inputs, outputs, initializers, nodes, and tensor dependencies
- `onnx-graph-practice/README.md`
  - explains the workflow and its relationship to AI compiler practice

## Operator and Graph Analysis

Resume description:

> Analyzed common operators such as Conv, MatMul, ReLU, and BatchNorm, and
> understood data flow and operator dependencies in the forward computation.

Repository evidence:

- `inspect_onnx_graph.py`
  - prints each ONNX node's operator type, inputs, and outputs
  - builds a simple producer-consumer view of tensor dependencies
- The tiny model includes linear layers and ReLU. Depending on exporter
  lowering, linear layers may appear as Gemm or MatMul/Add-style graph
  operations.

## AI Compiler Direction Exploration

Resume description:

> Initially learned AI compiler and inference optimization toolchains such as
> MLIR, TVM, and ONNX Runtime, and learned basic ideas such as operator fusion,
> constant folding, graph optimization, and backend adaptation.

Repository evidence:

- `docs/compiler_learning_notes.md`
  - connects compiler IR concepts with ONNX computation graphs
- `onnx-graph-practice/README.md`
  - summarizes graph-level optimization ideas such as constant folding,
    operator fusion, removing unused nodes, and backend-specific lowering

