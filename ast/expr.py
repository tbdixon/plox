from abc import ABC
from typing import List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ast.stmt import BlockStmt

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
        self.depth = None


class This(Expr):
    def __init__(self, this: Token):
        self.this = this
        self.depth = None


class Assign(Expr):
    def __init__(self, var: Variable, val: Expr):
        self.name = var.var.lexeme
        self.var = var
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


class LoxGet(Expr):
    def __init__(self, obj: Expr, name: Token):
        self.obj = obj
        self.name = name


class LoxSet(Expr):
    def __init__(self, obj: Expr, name: Token, val: Expr):
        self.obj = obj
        self.name = name
        self.val = val


class AnonymousFun(Expr):
    def __init__(self, params: List[Token], body: 'BlockStmt'):
        self.params = params
        self.body = body

