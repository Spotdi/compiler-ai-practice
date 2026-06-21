from __future__ import annotations

from dataclasses import dataclass


class Expr:
    pass


@dataclass(frozen=True)
class Number(Expr):
    value: int


@dataclass(frozen=True)
class Variable(Expr):
    name: str


@dataclass(frozen=True)
class BinaryOp(Expr):
    op: str
    left: Expr
    right: Expr


class Stmt:
    pass


@dataclass(frozen=True)
class LetStmt(Stmt):
    name: str
    expr: Expr


@dataclass(frozen=True)
class AssignStmt(Stmt):
    name: str
    expr: Expr


@dataclass(frozen=True)
class PrintStmt(Stmt):
    expr: Expr


@dataclass(frozen=True)
class Program:
    statements: list[Stmt]

