# Common Subexpression Elimination

## Motivation

Common subexpression elimination, usually shortened to CSE, avoids recomputing
the same expression when its operands have not changed.

Example:

```c
int a = x + y;
int b = x + y;
return a * b;
```

The expression `x + y` appears twice. If `x` and `y` are unchanged between the
two computations, the second computation can reuse the first result.

## Before Optimization

Example three-address IR:

```text
%1 = load x
%2 = load y
%3 = add %1, %2
store a, %3
%4 = load x
%5 = load y
%6 = add %4, %5
store b, %6
%7 = mul %3, %6
ret %7
```

## After Optimization

```text
%1 = load x
%2 = load y
%3 = add %1, %2
store a, %3
store b, %3
%7 = mul %3, %3
ret %7
```

## Pass-Level Idea

A basic CSE pass can maintain a table from expression keys to existing values.

An expression key may include:

- opcode, such as `add` or `mul`
- operand values
- type information
- flags that affect semantics

For commutative operations such as `add` and `mul`, the operands can be
canonicalized:

```text
add %x, %y
add %y, %x
```

These two expressions can use the same key if the operation is known to be
commutative.

## Safety Conditions

CSE is only valid when reusing the previous result preserves program behavior.

Important checks include:

- no operand value has changed
- no memory operation invalidates a loaded value
- the operation has no side effects
- floating-point flags and exception behavior are respected

## Local CSE vs Global CSE

Local CSE works inside one basic block. It is easier because instruction order
is simple.

Global CSE works across basic blocks. It requires control-flow and dominance
information. A value can be reused at another point only if the original
definition dominates that point.

## Relation to Compiler Pipeline

CSE is usually performed on IR after basic simplification. It often works well
with constant folding and dead code elimination: CSE may make some instructions
unused, and dead code elimination can remove them afterward.

