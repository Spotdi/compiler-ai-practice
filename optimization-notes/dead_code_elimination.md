# Dead Code Elimination

## Motivation

Dead code elimination removes computations that do not affect program output.

For example:

```c
int x = 1;
int y = x + 2;
return x;
```

The variable `y` is computed but never used. Removing it makes the program
smaller and may make later optimization passes easier.

## Before Optimization

Example three-address IR:

```text
%1 = const 1
store x, %1
%2 = load x
%3 = add %2, 2
store y, %3
%4 = load x
ret %4
```

## After Optimization

```text
%1 = const 1
store x, %1
%4 = load x
ret %4
```

If the compiler can also reason that `x` is constant, later passes may simplify
this even further:

```text
ret 1
```

## What Counts as Dead Code

An instruction is dead if:

- its result is not used, and
- it has no observable side effects.

Examples that are often safe to remove:

- unused arithmetic instructions
- unused comparisons
- unused temporary value conversions

Examples that should not be removed just because the result is unused:

- function calls that may have side effects
- stores to memory
- volatile loads or stores
- I/O operations

## Pass-Level Idea

A simple dead code elimination pass can work backward:

1. Mark side-effecting instructions and return values as live.
2. Mark all instructions needed to compute live values as live.
3. Remove unmarked instructions.

For SSA-style IR, use-def chains make this process easier because each value
has a clear definition and list of uses.

## Relation to Control Flow

Dead code elimination can also remove unreachable basic blocks. For example,
after constant folding:

```text
br false, label %then, label %else
```

can become:

```text
br label %else
```

Then `%then` may become unreachable and can be deleted from the control flow
graph.

## Relation to Compiler Pipeline

Dead code elimination is often repeated. Earlier passes may create dead code,
and removing it can make later passes cleaner and more effective.

