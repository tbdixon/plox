from interpreter.execute_expr import execute_expr
from multimethod.multimethod import multimethod
from interpreter.loxfunction import LoxFunction, FunctionType
from interpreter.loxclass import LoxClass
from environment.environment import LoxReturn
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
def execute_stmt(stmt: BlockStmt, env: Environment) -> None:
    stmt.env = Environment()
    stmt.env.outer_env = env
    for statement in stmt.statements:
        execute_stmt(statement, stmt.env)


@multimethod
def execute_stmt(stmt: IfStmt, env: Environment):
    if execute_expr(stmt.condition, env):
        return execute_stmt(stmt.then_branch, env)
    elif stmt.else_branch:
        return execute_stmt(stmt.else_branch, env)


@multimethod
def execute_stmt(stmt: WhileStmt, env: Environment) -> None:
    while execute_expr(stmt.condition, env):
        execute_stmt(stmt.body, env)


@multimethod
def execute_stmt(stmt: FunctionStmt, env: Environment) -> None:
    env.define(stmt.name.lexeme, LoxFunction(stmt, env, FunctionType.FUNCTION))


@multimethod
def execute_stmt(stmt: ReturnStmt, env: Environment):
    if stmt.value:
        ret_val = execute_expr(stmt.value, env)
    raise LoxReturn(ret_val)


@multimethod
def execute_stmt(stmt: ClassStmt, env: Environment):
    env.define(stmt.name.lexeme, None)
    methods = {method.name.lexeme: LoxFunction(method, env, FunctionType.METHOD) for method in stmt.methods}
    lox_class = LoxClass(stmt.name, methods)
    env.assign(stmt.name, lox_class, 0)
