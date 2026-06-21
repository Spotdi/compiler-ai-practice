# Constant Folding

## Motivation

Constant folding is a basic compiler optimization that evaluates expressions
whose operands are already known at compile time.

Instead of generating runtime instructions for:

```c
int x = 2 + 3 * 4;
```

the compiler can compute the result during compilation and replace the
expression with:

```c
int x = 14;
```

This reduces runtime work and may expose more opportunities for later
optimizations.

## Before Optimization

Example three-address IR:

```text
%1 = const 3
%2 = const 4
%3 = mul %1, %2
%4 = const 2
%5 = add %4, %3
store x, %5
```

## After Optimization

```text
%1 = const 14
store x, %1
```

## LLVM IR Style Example

Before:

```llvm
%a = mul i32 3, 4
%b = add i32 2, %a
ret i32 %b
```

After:

```llvm
ret i32 14
```

## Pass-Level Idea

A constant folding pass usually scans instructions and checks whether all
operands are compile-time constants.

For an instruction such as:

```text
%3 = add %1, %2
```

if `%1` and `%2` are both constants, the pass can:

1. calculate the result
2. replace all uses of `%3` with a new constant
3. remove the original instruction if it has no remaining users

## Important Details

- Integer overflow rules depend on the language and IR semantics.
- Floating-point folding must respect precision, NaN, rounding mode, and fast
  math flags.
- Folding may enable branch simplification. For example, `if (1 < 2)` can be
  simplified to an unconditional branch.

## Relation to Compiler Pipeline

Constant folding is normally performed after IR generation. It can also appear
in the frontend during AST simplification, but IR-level folding is more general
because it can use information produced by earlier analysis passes.

