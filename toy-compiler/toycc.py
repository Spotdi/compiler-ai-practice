from __future__ import annotations

import argparse
from pathlib import Path

from ir_generator import IRGenerator
from lexer import tokenize
from optimizer import optimize
from parser import Parser


def print_section(title: str, lines: list[str]) -> None:
    print(title)
    print("-" * len(title))
    for line in lines:
        print(line)
    print()


def compile_source(source: str) -> tuple[list[str], list[str], list[str]]:
    tokens = tokenize(source)
    program = Parser(tokens).parse()
    raw_ir = IRGenerator().generate(program)
    optimized_ir = optimize(raw_ir)
    return (
        [str(token) for token in tokens if token.kind != "EOF"],
        [str(instr) for instr in raw_ir],
        [str(instr) for instr in optimized_ir],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile a toy language to IR.")
    parser.add_argument("source", type=Path, help="Path to a .toy source file.")
    parser.add_argument(
        "--optimized-only",
        action="store_true",
        help="Print only the optimized IR.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source.read_text(encoding="utf-8")
    tokens, raw_ir, optimized_ir = compile_source(source)

    if args.optimized_only:
        print_section("Optimized IR", optimized_ir)
        return

    print_section("Tokens", tokens)
    print_section("Raw IR", raw_ir)
    print_section("Optimized IR", optimized_ir)


if __name__ == "__main__":
    main()

