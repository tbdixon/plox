from typing import List

from ast.expr import *
from scanner.token import Token
from scanner.tokentypes import TokenType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_idx = 0

    def current_token(self) -> Token:
        return self.tokens[self.current_token_idx]

    # Todo probably want some error checking here.
    def previous_token(self) -> Token:
        return self.tokens[self.current_token_idx - 1]

    def next_token(self):
        return self.tokens[self.current_token_idx + 1]

    def parse(self) -> Expr:
        return self.equality()

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
        if self.current_token().is_token_type([TokenType.TRUE]):
            self.current_token_idx += 1
            return Literal(True)
        if self.current_token().is_token_type([TokenType.NIL]):
            self.current_token_idx += 1
            return Literal(None)
        if self.current_token().is_token_type([TokenType.STRING, TokenType.NUMBER]):
            self.current_token_idx += 1
            return Literal(self.previous_token().literal)
        # Deal with grouping ()
