from typing import List

from ast.expr import InvalidExpr, Literal, Binary, Grouping, Unary
from ast.stmt import *
from error_handling.loxerror import LoxParseError
from scanner.token import Token
from scanner.tokentypes import TokenType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_idx = 0
        self.statements = []
        self.had_error = False
        self.error = None

    def is_at_end(self):
        return self.current_token().is_token_type([TokenType.EOF])

    def current_token(self) -> Token:
        return self.tokens[self.current_token_idx]

    def previous_token(self) -> Token:
        return self.tokens[self.current_token_idx - 1]

    def next_token(self):
        return self.tokens[self.current_token_idx + 1]

    def advance(self):
        self.current_token_idx += 1

    def check_consume_next(self, token_type: TokenType, error: str):
        if self.is_at_end() or not self.current_token().is_token_type([token_type]):
            self.had_error = True
            raise LoxParseError(error)
        self.advance()

    def match_type(self, token_types: List[TokenType]):
        return self.current_token().is_token_type(token_types)

    def parse(self) -> List[Stmt]:
        try:
            while not self.is_at_end():
                self.statements.append(self.statement())
        except LoxParseError as err:
            return [ExprStmt(InvalidExpr(err))]
        if self.had_error:
            return [ExprStmt(InvalidExpr(LoxParseError("Issue parsing", self.current_token())))]
        return self.statements

    def statement(self) -> Stmt:
        if self.match_type([TokenType.PRINT]):
            self.advance()
            return self.print_statement()
        else:
            return self.expr_statement()

    def expr_statement(self) -> Stmt:
        expr = self.expression()
        self.check_consume_next(TokenType.SEMICOLON, "Expect ';' after value.")
        return ExprStmt(expr)

    def print_statement(self) -> Stmt:
        expr = self.expression()
        self.check_consume_next(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(expr)

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match_type([TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL]):
            self.advance()
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def comparison(self) -> Expr:
        expr = self.addition()

        while self.match_type([TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL]):
            self.advance()
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def addition(self) -> Expr:
        expr = self.multiplication()

        while self.match_type([TokenType.PLUS, TokenType.MINUS]):
            self.advance()
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def multiplication(self) -> Expr:
        expr = self.unary()

        while self.match_type([TokenType.STAR, TokenType.SLASH]):
            self.advance()
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def unary(self) -> Expr:
        if self.match_type([TokenType.BANG, TokenType.MINUS]):
            self.advance()
            expr = Unary(self.previous_token(), self.unary())
        else:
            expr = self.primary()

        return expr

    def primary(self) -> Expr:
        if self.match_type([TokenType.FALSE]):
            self.advance()
            return Literal(False)
        elif self.match_type([TokenType.TRUE]):
            self.advance()
            return Literal(True)
        elif self.match_type([TokenType.NIL]):
            self.advance()
            return Literal(None)
        elif self.match_type([TokenType.STRING, TokenType.NUMBER]):
            self.advance()
            return Literal(self.previous_token().literal)
        elif self.match_type([TokenType.LEFT_PAREN]):
            self.advance()
            grouping_expr = Grouping(self.expression())
            if not self.match_type([TokenType.RIGHT_PAREN]):
                raise LoxParseError(f'Missing right paren', self.current_token())
            else:
                self.advance()
                return grouping_expr
        self.had_error = True
        raise LoxParseError(f'Invalid token found', self.current_token())
