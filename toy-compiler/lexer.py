from __future__ import annotations

from dataclasses import dataclass


KEYWORDS = {"let", "print"}
SINGLE_CHAR_TOKENS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "=": "EQUAL",
    "(": "LPAREN",
    ")": "RPAREN",
    ";": "SEMICOLON",
}


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    position: int

    def __str__(self) -> str:
        return f"{self.kind}({self.value!r})"


class LexerError(SyntaxError):
    pass


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0

    while i < len(source):
        ch = source[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit():
            start = i
            while i < len(source) and source[i].isdigit():
                i += 1
            tokens.append(Token("NUMBER", source[start:i], start))
            continue

        if ch.isalpha() or ch == "_":
            start = i
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1
            value = source[start:i]
            kind = value.upper() if value in KEYWORDS else "IDENT"
            tokens.append(Token(kind, value, start))
            continue

        kind = SINGLE_CHAR_TOKENS.get(ch)
        if kind:
            tokens.append(Token(kind, ch, i))
            i += 1
            continue

        raise LexerError(f"Unexpected character {ch!r} at position {i}")

    tokens.append(Token("EOF", "", len(source)))
    return tokens

