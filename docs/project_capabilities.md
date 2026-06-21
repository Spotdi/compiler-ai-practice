# Project Capabilities

This document summarizes the practical capabilities implemented in this
repository.

## Toy Compiler

The `toy-compiler/` module implements a compact compiler pipeline for a small
expression language.

Implemented stages:

- lexical analysis
- recursive-descent parsing
- AST construction
- semantic checks for declaration-before-use
- three-address IR generation
- constant folding
- simple dead code elimination

Supported language features:

- `let` declarations
- assignments
- `print(...)`
- integer literals
- variables
- `+`, `-`, `*`, `/`
- parentheses and operator precedence

This module provides a concrete implementation of frontend and middle-end
compiler concepts.

## LLVM IR Examples

The LLVM IR examples are designed to make high-level control-flow constructs
visible at the IR level.

Implemented examples:

- integer arithmetic
- conditional branches
- loops with `phi` nodes
- function definitions and calls

These examples are useful for understanding how compiler frontends lower source
constructs into an intermediate representation.

## Optimization Notes

The optimization notes explain classic compiler transformations:

- constant folding
- dead code elimination
- common subexpression elimination

Each note focuses on:

- the problem the optimization solves
- before/after IR examples
- pass-level implementation ideas
- safety conditions

## ONNX Graph Inspection

The ONNX graph inspector is the most practical tool in this repository. It can
be used to inspect a small exported model or any compatible ONNX model.

Current capabilities:

- validate an ONNX model with `onnx.checker`
- list graph inputs and outputs
- list initializers and parameter shapes
- count operators by type
- count total parameters
- print every node with inputs and outputs
- build producer-consumer tensor dependencies
- detect unused initializers and unused node outputs
- identify simple fusion candidates
- export a JSON report
- export a Graphviz DOT graph

## Practical Use Cases

The graph inspector helps answer questions that commonly appear before model
deployment:

- Does this model use operators supported by my backend?
- Which operators dominate the graph?
- Which weights and constants are stored as initializers?
- Are there graph artifacts that appear unused?
- Are there simple producer-consumer patterns that a backend could fuse?
- Can I create a graph visualization for debugging or documentation?

## Limitations

The project intentionally stays compact. It does not perform full ONNX graph
rewriting, shape inference for all intermediate tensors, or backend-specific
lowering. The current focus is analysis and explanation rather than production
optimization.

Potential extensions:

- add ONNX shape inference output
- implement a real graph rewrite pass
- export optimized ONNX models
- benchmark inference with ONNX Runtime
- support larger model summaries
