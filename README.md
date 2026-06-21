# Compiler AI Practice

A compact compiler and AI graph analysis project focused on frontend
implementation, intermediate representation, optimization principles, LLVM IR,
and practical ONNX model inspection.

The repository is built around one idea: compiler techniques are useful beyond
traditional programming languages. The same concepts behind IR, control flow,
data flow, and optimization passes also appear in AI model deployment and graph
optimization.

## Highlights

- Handwritten LLVM IR examples for arithmetic, branches, loops, and function
  calls.
- A small toy compiler with lexer, parser, AST, semantic checks, IR generation,
  constant folding, and simple dead code elimination.
- Clear notes for constant folding, dead code elimination, and common
  subexpression elimination.
- A practical ONNX graph inspector that reports operators, parameters, tensor
  dependencies, unused graph artifacts, and simple fusion candidates.
- Optional JSON and Graphviz DOT output for model analysis and visualization.

## Repository Layout

```text
.
├── README.md
├── toy-compiler/
│   ├── ast_nodes.py
│   ├── lexer.py
│   ├── parser.py
│   ├── ir.py
│   ├── ir_generator.py
│   ├── optimizer.py
│   ├── toycc.py
│   ├── examples/
│   │   └── demo.toy
│   └── README.md
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
    └── project_capabilities.md
```

## What This Project Can Do

### 1. Compile a Small Toy Language

`toy-compiler/` implements a small compiler pipeline:

```text
source -> tokens -> AST -> three-address IR -> optimized IR
```

It supports declarations, assignments, `print`, integer expressions, operator
precedence, semantic checks, constant folding, and simple dead code
elimination.

Example:

```bash
cd toy-compiler
python3 toycc.py examples/demo.toy
```

Input:

```text
let x = 1 + 2 * 3;
let y = x + 4;
let unused = 10 * 20;
print(y);
```

Optimized IR:

```text
print 11
```

### 2. Inspect AI Model Graphs

`onnx-graph-practice/inspect_onnx_graph.py` turns an ONNX file into a readable
graph analysis report.

It can answer practical questions such as:

- Which operators does the model use?
- How many parameters does it contain?
- Which tensors connect producer and consumer nodes?
- Are there unused initializers or node outputs?
- Are there simple fusion opportunities such as `Gemm -> Relu`,
  `MatMul -> Add`, or `Conv -> BatchNormalization -> Relu`?
- Can the graph be exported to DOT for visualization?

Example:

```bash
cd onnx-graph-practice
python inspect_onnx_graph.py tiny_model.onnx \
  --json graph_report.json \
  --dot graph.dot
```

### 3. Practice LLVM IR

The `llvm-ir-practice/` directory shows how common high-level constructs are
represented in LLVM IR:

- arithmetic
- if/else branches
- loops and `phi` nodes
- function calls

Run with LLVM:

```bash
cd llvm-ir-practice
lli 01_arithmetic.ll
```

Or compile with `clang`:

```bash
clang 01_arithmetic.ll -o arithmetic
./arithmetic
echo $?
```

### 4. Explain Optimization Passes

The `optimization-notes/` directory explains classic compiler optimizations in
a way that connects directly to IR transformation:

- constant folding
- dead code elimination
- common subexpression elimination

These notes focus on optimization motivation, before/after examples, pass-level
logic, and safety conditions.

## Quick Start

### Run the Toy Compiler

```bash
cd /path/to/compiler-ai-practice/toy-compiler
python3 toycc.py examples/demo.toy
python3 -m unittest discover -s tests
```

### Run the ONNX Graph Tool

```bash
cd /path/to/compiler-ai-practice
python3 -m venv .venv
source .venv/bin/activate
pip install -r onnx-graph-practice/requirements.txt

cd onnx-graph-practice
python export_tiny_model.py
python inspect_onnx_graph.py tiny_model.onnx
```

Generate machine-readable and visualization outputs:

```bash
python inspect_onnx_graph.py tiny_model.onnx \
  --json graph_report.json \
  --dot graph.dot
```

## Example Output

The toy compiler prints raw and optimized IR:

```text
Raw IR
------
t0 = 2 * 3
t1 = 1 + t0
x = t1
t2 = x + 4
y = t2
t3 = 10 * 20
unused = t3
print y

Optimized IR
------------
print 11
```

The ONNX inspector prints sections like:

```text
Operator Summary
----------------
Gemm: 2
Relu: 1

Parameter Summary
-----------------
total initializers: 4
total parameters : 23

Fusion Candidates
-----------------
[0 -> 1] node_linear_0 (Gemm) -> node_relu_1 (Relu): activation fusion candidate
```

## Why This Is Useful

Before deploying an ONNX model to an inference backend, engineers often need to
understand the graph structure:

- backend compatibility depends on operator coverage
- optimization depends on producer-consumer patterns
- memory and performance depend on tensor flow and parameter size
- graph simplification depends on identifying unused values and fusable
  subgraphs

This project demonstrates those compiler-style analysis ideas with small,
runnable examples.

## Documentation

- [docs/compiler_learning_notes.md](docs/compiler_learning_notes.md): compiler
  pipeline notes.
- [docs/project_capabilities.md](docs/project_capabilities.md): what the
  project implements and what problems it can help solve.
