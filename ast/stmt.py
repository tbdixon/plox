from abc import ABC
from typing import List

from ast.expr import Expr
from scanner.token import Token
from environment.environment import Environment


class Stmt(ABC):
    pass


class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression


class ExprStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression


class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer


class AssignStmt(Stmt):
    def __init__(self, name: Token, value: Expr = None):
        self.name = name
        self.value = value


class BlockStmt(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements = statements
        self.env = Environment()


class InvalidStmt(Stmt):
    pass
