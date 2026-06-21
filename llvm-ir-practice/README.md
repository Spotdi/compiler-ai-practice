# LLVM IR Practice

This directory contains handwritten LLVM IR examples. The goal is to understand
how common source-level constructs are represented in a lower-level
intermediate representation.

## Files

- `01_arithmetic.ll`: integer arithmetic and return value
- `02_if_else.ll`: conditional branch with two basic blocks
- `03_loop.ll`: loop control flow with `phi`
- `04_function_call.ll`: function definition and function call

## Run With `lli`

```bash
lli 01_arithmetic.ll
echo $?
```

The process exit code is the integer returned by `main`.

Run all examples:

```bash
for f in *.ll; do
  echo "Running $f"
  lli "$f"
  echo "exit code: $?"
done
```

## Compile With `clang`

```bash
clang 01_arithmetic.ll -o arithmetic
./arithmetic
echo $?
```

## Key LLVM IR Concepts

- `define`: defines a function.
- `add`, `sub`, `mul`, `sdiv`: integer arithmetic instructions.
- `icmp`: integer comparison instruction.
- `br`: branch instruction.
- `phi`: selects a value depending on the predecessor basic block.
- `call`: calls another function.
- `ret`: returns from a function.

