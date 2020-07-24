from interpreter.execute_expr import execute_expr
from multimethod.multimethod import multimethod
from environment.environment import Environment
from ast.stmt import *


@multimethod
def execute_stmt(stmt: ExprStmt, env: Environment) -> None:
    execute_expr(stmt.expression, env)


@multimethod
def execute_stmt(stmt: PrintStmt, env: Environment) -> None:
    print(execute_expr(stmt.expression, env))


@multimethod
def execute_stmt(stmt: VarStmt, env: Environment) -> None:
    init_val = None
    if stmt.initializer:
        init_val = execute_expr(stmt.initializer, env)
    env.define(stmt.name.lexeme, init_val)
