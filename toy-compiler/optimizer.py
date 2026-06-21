from __future__ import annotations

from ir import AssignInstr, BinaryInstr, Const, Instruction, Name, PrintInstr, Value


def fold_binary(op: str, left: int, right: int) -> int:
    if op == "+":
        return left + right
    if op == "-":
        return left - right
    if op == "*":
        return left * right
    if op == "/":
        if right == 0:
            raise ZeroDivisionError("Division by zero during constant folding.")
        return left // right
    raise ValueError(f"Unsupported binary operator: {op}")


def replace_value(value: Value, constants: dict[str, Const]) -> Value:
    if isinstance(value, Name) and value.value in constants:
        return constants[value.value]
    return value


def constant_fold(instructions: list[Instruction]) -> list[Instruction]:
    constants: dict[str, Const] = {}
    folded: list[Instruction] = []

    for instr in instructions:
        if isinstance(instr, BinaryInstr):
            left = replace_value(instr.left, constants)
            right = replace_value(instr.right, constants)
            if isinstance(left, Const) and isinstance(right, Const):
                result = Const(fold_binary(instr.op, left.value, right.value))
                constants[instr.target] = result
                folded.append(AssignInstr(instr.target, result))
            else:
                constants.pop(instr.target, None)
                folded.append(BinaryInstr(instr.target, instr.op, left, right))
            continue

        if isinstance(instr, AssignInstr):
            value = replace_value(instr.value, constants)
            if isinstance(value, Const):
                constants[instr.target] = value
            else:
                constants.pop(instr.target, None)
            folded.append(AssignInstr(instr.target, value))
            continue

        if isinstance(instr, PrintInstr):
            folded.append(PrintInstr(replace_value(instr.value, constants)))
            continue

    return folded


def used_names(value: Value) -> set[str]:
    if isinstance(value, Name):
        return {value.value}
    return set()


def dead_code_eliminate(instructions: list[Instruction]) -> list[Instruction]:
    live: set[str] = set()
    kept_reversed: list[Instruction] = []

    for instr in reversed(instructions):
        if isinstance(instr, PrintInstr):
            live.update(used_names(instr.value))
            kept_reversed.append(instr)
            continue

        if isinstance(instr, BinaryInstr):
            if instr.target in live:
                live.remove(instr.target)
                live.update(used_names(instr.left))
                live.update(used_names(instr.right))
                kept_reversed.append(instr)
            continue

        if isinstance(instr, AssignInstr):
            if instr.target in live:
                if instr.target in live:
                    live.remove(instr.target)
                live.update(used_names(instr.value))
                kept_reversed.append(instr)
            continue

    return list(reversed(kept_reversed))


def optimize(instructions: list[Instruction]) -> list[Instruction]:
    return dead_code_eliminate(constant_fold(instructions))
