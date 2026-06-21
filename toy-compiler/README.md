# Toy Compiler

This directory implements a compact compiler frontend and middle-end for a
small expression language.

It is intentionally small, but it contains the core pieces of a compiler:

- lexer
- parser
- AST nodes
- semantic checks
- three-address IR generation
- constant folding
- simple dead code elimination

## Language Features

Supported statements:

```text
let x = 1 + 2 * 3;
x = x + 4;
print(x);
```

Supported expressions:

- integer literals
- variables
- `+`, `-`, `*`, `/`
- parentheses

## Run

From this directory:

```bash
python3 toycc.py examples/demo.toy
```

Show only optimized IR:

```bash
python3 toycc.py examples/demo.toy --optimized-only
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## Example Output

```text
Tokens
------
LET('let')
IDENT('x')
...

Raw IR
------
t0 = 2 * 3
t1 = 1 + t0
x = t1
t2 = x + 4
y = t2
print y

Optimized IR
------------
print 11
```

## Why This Matters

This module shows how source code can be transformed through compiler stages:

```text
source -> tokens -> AST -> IR -> optimized IR
```

The implementation is small enough to read in one sitting, but it still maps to
real compiler concepts used in larger systems.
