from abc import ABC
from typing import List

from scanner.token import Token


class Expr(ABC):
    def __str__(self):
        return ' '.join([f'{attr}: [{val}]' for attr, val in vars(self).items()])


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


class Assign(Expr):
    def __init__(self, name: Token, val):
        self.name = name
        self.val = val


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments
