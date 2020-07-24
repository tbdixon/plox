from abc import ABC
from ast.expr import Expr
from scanner.token import Token


class Stmt(ABC):
    pass


class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression


class ExprStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression


class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Expr = None):
        self.name = name
        self.initializer = initializer
