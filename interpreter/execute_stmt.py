from interpreter.execute_expr import execute_expr
from multimethod.multimethod import multimethod
from ast.stmt import *


@multimethod
def execute_stmt(stmt: ExprStmt) -> None:
    execute_expr(stmt.expression)


@multimethod
def execute_stmt(stmt: PrintStmt) -> None:
    print(execute_expr(stmt.expression))