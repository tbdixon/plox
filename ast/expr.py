from abc import ABC
from scanner.token import Token
from error_handling.loxerror import LoxError


class Expr(ABC):
    def __str__(self):
        return ' '.join([f'{attr}: [{val}]' for attr, val in vars(self).items()])


class InvalidExpr(Expr):
    def __init__(self, error: LoxError):
        self.error = error


class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Unary(Expr):
    def __init__(self, operator: Token, expression: Expr):
        self.operator = operator
        self.right = expression


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression


class Variable(Expr):
    def __init__(self, var: Token):
        self.var = var
