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


@multimethod
def execute_stmt(stmt: AssignStmt, env: Environment) -> None:
    env.assign(stmt.name, execute_expr(stmt.value, env))


@multimethod
def execute_stmt(stmt: BlockStmt, env: Environment) -> None:
    stmt.env = Environment()
    stmt.env.outer_env = env
    for statement in stmt.statements:
        execute_stmt(statement, stmt.env)

@multimethod
def execute_stmt(stmt: IfStmt, env: Environment) -> None:
    condition = execute_expr(stmt.condition, env)
    if condition:
        return execute_stmt(stmt.then_branch, env)
    elif stmt.else_branch:
        return execute_stmt(stmt.else_branch, env)
