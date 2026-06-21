# Compiler Learning Notes

This document summarizes the compiler concepts practiced in this repository.

## 1. Compiler Pipeline

A typical compiler pipeline can be viewed as:

```text
source code
  -> lexical analysis
  -> syntax analysis
  -> AST
  -> semantic analysis
  -> IR generation
  -> optimization passes
  -> code generation
```

Each stage changes the representation of the program and exposes different
information to the compiler.

## 2. Lexical Analysis

Lexical analysis converts source code characters into tokens.

Example:

```c
let x = 1 + 2;
```

Possible token sequence:

```text
KEYWORD(let)
IDENT(x)
ASSIGN(=)
NUMBER(1)
PLUS(+)
NUMBER(2)
SEMICOLON(;)
```

The lexer does not fully understand program structure. It mainly recognizes
small meaningful units.

## 3. Syntax Analysis

Syntax analysis checks whether tokens follow the grammar of the language and
builds a syntax tree or AST.

For:

```c
1 + 2 * 3
```

the parser should preserve precedence:

```text
Add
├── Number(1)
└── Mul
    ├── Number(2)
    └── Number(3)
```

## 4. AST

The abstract syntax tree removes unnecessary syntax details and keeps the
program structure.

Common AST node categories include:

- expressions: literal, variable, binary operation, function call
- statements: assignment, if, while, return
- declarations: variable declaration, function declaration

The AST is usually easier to analyze than raw tokens.

## 5. Semantic Analysis and Symbol Table

Semantic analysis checks rules that are not fully captured by syntax.

Examples:

- whether a variable is declared before use
- whether a function call has the correct number of arguments
- whether expression types are compatible

A symbol table records names and their related information, such as variable
type, scope, and storage location.

## 6. Intermediate Representation

An intermediate representation, or IR, is a lower-level program representation
used by compiler middle-end optimizations.

Compared with source code, IR is usually:

- more explicit
- easier to analyze
- closer to machine-level operations
- independent from the original source language

LLVM IR is a well-known IR. It uses typed instructions and basic blocks.

## 7. Basic Blocks and Control Flow Graph

A basic block is a straight-line sequence of instructions with:

- one entry point
- one exit point
- no internal branch target

A control flow graph, or CFG, connects basic blocks using branch edges.

Example if-else CFG:

```text
entry
  ├── then
  └── else
        \ 
         merge
```

CFG is important for branch analysis, loop analysis, dominance analysis, and
many optimization passes.

## 8. Optimization Passes

An optimization pass reads and transforms IR.

Examples in this repository:

- constant folding
- dead code elimination
- common subexpression elimination

Optimization passes often work together. Constant folding can simplify a
branch, which may create unreachable code, which dead code elimination can then
remove.

## 9. Code Generation

Code generation lowers IR to a target representation.

Possible targets include:

- assembly
- machine code
- bytecode
- another IR

In this repository, handwritten LLVM IR examples are used to understand how
high-level constructs can be represented before final lowering.

## 10. AI Compiler and Computation Graphs

AI model deployment also uses IR-like ideas. A trained model can be exported
from PyTorch into ONNX, where the model becomes a computation graph.

In this graph:

- nodes represent operators such as MatMul, Add, Relu, Conv, or BatchNorm
- edges represent tensors
- initializers represent weights and constants

Graph-level optimization can include:

- operator fusion
- constant folding
- removing unused nodes
- lowering graph operators to backend-specific kernels

This is why compiler concepts such as IR, graph analysis, and optimization
passes are useful for AI deployment and inference acceleration.

