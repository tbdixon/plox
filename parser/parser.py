from typing import List

from ast.expr import *
from error_handling.error import ParseError
from scanner.token import Token
from scanner.tokentypes import TokenType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_idx = 0
        self.had_error = False

    def is_at_end(self):
        return self.current_token().is_token_type([TokenType.EOF])

    def current_token(self) -> Token:
        return self.tokens[self.current_token_idx]

    def previous_token(self) -> Token:
        return self.tokens[self.current_token_idx - 1]

    def next_token(self):
        return self.tokens[self.current_token_idx + 1]

    def parse(self) -> Expr:
        expr = self.expression()
        if self.is_at_end():
            return expr
        else:
            return InvalidExpr(ParseError("Incomplete parsing", self.current_token()))

    def expression(self) -> Expr:
        try:
            return self.equality()
        except ParseError as err:
            return InvalidExpr(err)

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.tokens[self.current_token_idx].is_token_type([TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL]):
            self.current_token_idx += 1
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def comparison(self) -> Expr:
        expr = self.addition()

        while self.tokens[self.current_token_idx].is_token_type(
                [TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL]):
            self.current_token_idx += 1
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def addition(self) -> Expr:
        expr = self.multiplication()

        while self.tokens[self.current_token_idx].is_token_type([TokenType.PLUS, TokenType.MINUS]):
            self.current_token_idx += 1
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def multiplication(self) -> Expr:
        expr = self.unary()

        while self.tokens[self.current_token_idx].is_token_type([TokenType.STAR, TokenType.SLASH]):
            self.current_token_idx += 1
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def unary(self) -> Expr:
        if self.tokens[self.current_token_idx].is_token_type([TokenType.BANG, TokenType.MINUS]):
            self.current_token_idx += 1
            expr = Unary(self.previous_token(), self.unary())
        else:
            expr = self.primary()

        return expr

    def primary(self) -> Expr:
        if self.current_token().is_token_type([TokenType.FALSE]):
            self.current_token_idx += 1
            return Literal(False)
        elif self.current_token().is_token_type([TokenType.TRUE]):
            self.current_token_idx += 1
            return Literal(True)
        elif self.current_token().is_token_type([TokenType.NIL]):
            self.current_token_idx += 1
            return Literal(None)
        elif self.current_token().is_token_type([TokenType.STRING, TokenType.NUMBER]):
            self.current_token_idx += 1
            return Literal(self.previous_token().literal)
        elif self.current_token().is_token_type([TokenType.LEFT_PAREN]):
            #TODO: need to verify the closing paren is present
            self.current_token_idx += 1
            return Grouping(self.expression())
        self.had_error = True
        raise ParseError(f'Invalid token found', self.current_token())
