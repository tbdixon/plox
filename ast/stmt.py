from abc import ABC
from ast.expr import Expr


class Stmt(ABC):
    pass


class PrintStmt(Stmt):
    def __init(self, expression: Expr):
        self.expression = expression


class ExprStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression
