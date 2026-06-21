from __future__ import annotations

from ast_nodes import AssignStmt, BinaryOp, Expr, LetStmt, Number, PrintStmt, Program, Stmt, Variable
from lexer import Token


class ParserError(SyntaxError):
    pass


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements: list[Stmt] = []
        while not self.check("EOF"):
            statements.append(self.statement())
        return Program(statements)

    def statement(self) -> Stmt:
        if self.match("LET"):
            name = self.consume("IDENT", "Expected variable name after 'let'.")
            self.consume("EQUAL", "Expected '=' after variable name.")
            expr = self.expression()
            self.consume("SEMICOLON", "Expected ';' after declaration.")
            return LetStmt(name.value, expr)

        if self.match("PRINT"):
            self.consume("LPAREN", "Expected '(' after 'print'.")
            expr = self.expression()
            self.consume("RPAREN", "Expected ')' after print expression.")
            self.consume("SEMICOLON", "Expected ';' after print statement.")
            return PrintStmt(expr)

        if self.check("IDENT") and self.peek_next().kind == "EQUAL":
            name = self.advance()
            self.consume("EQUAL", "Expected '=' after variable name.")
            expr = self.expression()
            self.consume("SEMICOLON", "Expected ';' after assignment.")
            return AssignStmt(name.value, expr)

        token = self.peek()
        raise ParserError(f"Unexpected token {token.kind} at position {token.position}")

    def expression(self) -> Expr:
        return self.term()

    def term(self) -> Expr:
        expr = self.factor()
        while self.match("PLUS", "MINUS"):
            op = self.previous().value
            right = self.factor()
            expr = BinaryOp(op, expr, right)
        return expr

    def factor(self) -> Expr:
        expr = self.primary()
        while self.match("STAR", "SLASH"):
            op = self.previous().value
            right = self.primary()
            expr = BinaryOp(op, expr, right)
        return expr

    def primary(self) -> Expr:
        if self.match("NUMBER"):
            return Number(int(self.previous().value))

        if self.match("IDENT"):
            return Variable(self.previous().value)

        if self.match("LPAREN"):
            expr = self.expression()
            self.consume("RPAREN", "Expected ')' after expression.")
            return expr

        token = self.peek()
        raise ParserError(f"Expected expression at position {token.position}")

    def match(self, *kinds: str) -> bool:
        for kind in kinds:
            if self.check(kind):
                self.advance()
                return True
        return False

    def consume(self, kind: str, message: str) -> Token:
        if self.check(kind):
            return self.advance()
        token = self.peek()
        raise ParserError(f"{message} Got {token.kind} at position {token.position}")

    def check(self, kind: str) -> bool:
        return self.peek().kind == kind

    def advance(self) -> Token:
        if not self.check("EOF"):
            self.current += 1
        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def peek_next(self) -> Token:
        if self.current + 1 >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.current + 1]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

