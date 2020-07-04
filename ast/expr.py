from abc import ABC
from scanner.token import Token


class Expr(ABC):
    pass


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
