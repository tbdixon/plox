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


class IfStmt(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body


class FunctionStmt(Stmt):
    def __init__(self, name: Token, params: List[Token], body: BlockStmt):
        self.name = name
        self.params = params
        self.body = body


class InvalidStmt(Stmt):
    pass
