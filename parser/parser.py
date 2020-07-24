from typing import List

from ast.expr import Literal, Binary, Grouping, Unary, Variable
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
        self.errors = []

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
            raise LoxParseError(error, self.previous_token())
        self.advance()

    def advance_if_match(self, token_types: List[TokenType]):
        if self.current_token().is_token_type(token_types):
            self.advance()
            return True
        return False

    def synchronize(self):
        pass

    def parse(self) -> List[Stmt]:
        while not self.is_at_end():
            self.statements.append(self.declaration())
        return self.statements

    def declaration(self) -> Stmt:
        try:
            if self.advance_if_match([TokenType.VAR]):
                return self.var_declaration()
            return self.statement()
        except LoxParseError as err:
            self.synchronize()
            self.had_error = True
            self.errors.append(err)

    def var_declaration(self) -> Stmt:
        var_name = self.current_token()
        expr = None
        self.check_consume_next(TokenType.IDENTIFIER, "Missing variable name")
        if self.advance_if_match([TokenType.EQUAL]):
            expr = self.expression()
        self.check_consume_next(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return VarStmt(var_name, expr)

    def statement(self) -> Stmt:
        if self.advance_if_match([TokenType.PRINT]):
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

        while self.advance_if_match([TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL]):
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def comparison(self) -> Expr:
        expr = self.addition()

        while self.advance_if_match([TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL]):
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def addition(self) -> Expr:
        expr = self.multiplication()

        while self.advance_if_match([TokenType.PLUS, TokenType.MINUS]):
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def multiplication(self) -> Expr:
        expr = self.unary()

        while self.advance_if_match([TokenType.STAR, TokenType.SLASH]):
            expr = Binary(expr, self.previous_token(), self.comparison())

        return expr

    def unary(self) -> Expr:
        if self.advance_if_match([TokenType.BANG, TokenType.MINUS]):
            expr = Unary(self.previous_token(), self.unary())
        else:
            expr = self.primary()

        return expr

    def primary(self) -> Expr:
        if self.advance_if_match([TokenType.FALSE]):
            return Literal(False)
        elif self.advance_if_match([TokenType.TRUE]):
            return Literal(True)
        elif self.advance_if_match([TokenType.NIL]):
            return Literal(None)
        elif self.advance_if_match([TokenType.STRING, TokenType.NUMBER]):
            return Literal(self.previous_token().literal)
        elif self.advance_if_match([TokenType.IDENTIFIER]):
            return Variable(self.previous_token())
        elif self.advance_if_match([TokenType.LEFT_PAREN]):
            grouping_expr = Grouping(self.expression())
            if not self.advance_if_match([TokenType.RIGHT_PAREN]):
                raise LoxParseError(f'Missing right paren', self.current_token())
            else:
                return grouping_expr
        raise LoxParseError(f'Invalid token found', self.current_token())
