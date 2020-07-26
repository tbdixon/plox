from typing import List

from ast.expr import Literal, Binary, Grouping, Unary, Variable, Assign, Logical
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

    def check(self, token_types: List[TokenType]):
        return self.current_token().is_token_type(token_types)

    def advance_if_match(self, token_types: List[TokenType]):
        if self.current_token().is_token_type(token_types):
            self.advance()
            return True
        return False

    def synchronize(self):
        while not self.is_at_end() and not self.check([TokenType.SEMICOLON]):
            self.advance()
        self.advance()

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
            return InvalidStmt

    def var_declaration(self) -> Stmt:
        var_name = self.current_token()
        expr = None
        self.check_consume_next(TokenType.IDENTIFIER, "Missing variable name")
        if self.advance_if_match([TokenType.EQUAL]):
            expr = self.expression()
        self.check_consume_next(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return VarStmt(var_name, expr)

    def statement(self) -> Stmt:
        match = {
            TokenType.PRINT: self.print_statement,
            TokenType.LEFT_BRACE: self.block_statement,
            TokenType.IF: self.if_statement,
            TokenType.WHILE: self.while_statement
        }
        token_type = self.current_token().tokentype
        fn = match.get(token_type, None)
        if fn:
            self.advance()
            return fn()
        else:
            return self.expr_statement()

    def while_statement(self):
        self.check_consume_next(TokenType.LEFT_PAREN, "Missing left parentheses")
        condition = self.expression()
        self.check_consume_next(TokenType.RIGHT_PAREN, "Missing left parentheses")
        body = self.statement()
        return WhileStmt(condition, body)


    def block_statement(self) -> BlockStmt:
        statements = []
        while not self.is_at_end() and not self.check([TokenType.RIGHT_BRACE]):
            statements.append(self.declaration())
        self.check_consume_next(TokenType.RIGHT_BRACE, "Missing closing brace")
        return BlockStmt(statements)

    def expr_statement(self) -> ExprStmt:
        expr = self.expression()
        self.check_consume_next(TokenType.SEMICOLON, "Expect ';' after value.")
        return ExprStmt(expr)

    def print_statement(self) -> PrintStmt:
        expr = self.expression()
        self.check_consume_next(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(expr)

    def if_statement(self) -> IfStmt:
        self.check_consume_next(TokenType.LEFT_PAREN, "Missing left parentheses")
        condition = self.expression()
        self.check_consume_next(TokenType.RIGHT_PAREN, "Missing right parentheses")
        then_branch = self.statement()
        if_stmt = IfStmt(condition, then_branch)
        if self.advance_if_match([TokenType.ELSE]):
            if_stmt.else_branch = self.statement()
        return if_stmt

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        val = self.logical_or()
        if self.advance_if_match([TokenType.EQUAL]):
            r_value = self.assignment()
            if type(val) == Variable:
                return Assign(val.var, r_value)
            else:
                raise LoxParseError(f'Invalid assignment target {self.previous_token().lexeme}')
        return val

    def logical_or(self) -> Expr:
        expr = self.logical_and()
        while self.advance_if_match([TokenType.OR]):
            operator = self.previous_token()
            right = self.logical_and()
            expr = Logical(expr, operator, right)
        return expr

    def logical_and(self) -> Expr:
        expr = self.equality()
        while self.advance_if_match([TokenType.AND]):
            operator = self.previous_token()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

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

    def grouping_helper(self):
        grouping_expr = Grouping(self.expression())
        if not self.advance_if_match([TokenType.RIGHT_PAREN]):
            raise LoxParseError(f'Missing right paren', self.current_token())
        else:
            return grouping_expr

    def primary(self) -> Expr:
        match = {
            TokenType.FALSE: lambda: Literal(False),
            TokenType.TRUE: lambda: Literal(True),
            TokenType.NIL: lambda: Literal(None),
            TokenType.STRING: lambda: Literal(self.previous_token().literal),
            TokenType.NUMBER: lambda: Literal(self.previous_token().literal),
            TokenType.IDENTIFIER: lambda: Variable(self.previous_token()),
            TokenType.LEFT_PAREN: self.grouping_helper
        }
        token_type = self.current_token().tokentype
        fn = match.get(token_type, None)
        self.advance()
        if fn:
            return fn()
        else:
            raise LoxParseError(f'Invalid token found', self.current_token())
