from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Const:
    value: int

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Name:
    value: str

    def __str__(self) -> str:
        return self.value


Value = Const | Name


@dataclass(frozen=True)
class BinaryInstr:
    target: str
    op: str
    left: Value
    right: Value

    def __str__(self) -> str:
        return f"{self.target} = {self.left} {self.op} {self.right}"


@dataclass(frozen=True)
class AssignInstr:
    target: str
    value: Value

    def __str__(self) -> str:
        return f"{self.target} = {self.value}"


@dataclass(frozen=True)
class PrintInstr:
    value: Value

    def __str__(self) -> str:
        return f"print {self.value}"


Instruction = BinaryInstr | AssignInstr | PrintInstr

