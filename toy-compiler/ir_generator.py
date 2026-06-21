from __future__ import annotations

from ast_nodes import AssignStmt, BinaryOp, Expr, LetStmt, Number, PrintStmt, Program, Stmt, Variable
from ir import AssignInstr, BinaryInstr, Const, Instruction, Name, PrintInstr, Value


class SemanticError(Exception):
    pass


class IRGenerator:
    def __init__(self) -> None:
        self.instructions: list[Instruction] = []
        self.symbols: set[str] = set()
        self.temp_counter = 0

    def generate(self, program: Program) -> list[Instruction]:
        for stmt in program.statements:
            self.emit_stmt(stmt)
        return self.instructions

    def emit_stmt(self, stmt: Stmt) -> None:
        if isinstance(stmt, LetStmt):
            value = self.emit_expr(stmt.expr)
            self.symbols.add(stmt.name)
            self.instructions.append(AssignInstr(stmt.name, value))
            return

        if isinstance(stmt, AssignStmt):
            if stmt.name not in self.symbols:
                raise SemanticError(f"Variable {stmt.name!r} assigned before declaration.")
            value = self.emit_expr(stmt.expr)
            self.instructions.append(AssignInstr(stmt.name, value))
            return

        if isinstance(stmt, PrintStmt):
            value = self.emit_expr(stmt.expr)
            self.instructions.append(PrintInstr(value))
            return

        raise SemanticError(f"Unsupported statement: {stmt!r}")

    def emit_expr(self, expr: Expr) -> Value:
        if isinstance(expr, Number):
            return Const(expr.value)

        if isinstance(expr, Variable):
            if expr.name not in self.symbols:
                raise SemanticError(f"Variable {expr.name!r} used before declaration.")
            return Name(expr.name)

        if isinstance(expr, BinaryOp):
            left = self.emit_expr(expr.left)
            right = self.emit_expr(expr.right)
            target = self.new_temp()
            self.instructions.append(BinaryInstr(target, expr.op, left, right))
            return Name(target)

        raise SemanticError(f"Unsupported expression: {expr!r}")

    def new_temp(self) -> str:
        name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return name
