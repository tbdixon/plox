from collections import deque

from multimethod.multimethod import multimethod
from ast.stmt import *
from ast.expr import *


def start_scope(scopes: deque) -> deque:
    scopes.appendleft({})
    return scopes


def end_scope(scopes: deque) -> deque:
    scopes.popleft()
    return scopes


def get_depth(var: str, scopes: deque) -> int:
    depth = 0
    for scope in scopes:
        if var in scope:
            return depth
        depth += 1
    return depth


def declare(name: Token, scopes: deque):
    if len(scopes):
        scopes[0][name.lexeme] = False


def define(name: Token, scopes: deque):
    if len(scopes):
        scopes[0][name.lexeme] = True


@multimethod
def resolve(variable: Variable, scopes: deque):
    variable.depth = get_depth(variable.var.lexeme, scopes)


@multimethod
def resolve(assignment: Assign, scopes: deque):
    resolve(assignment.val, scopes)
    assignment.var.depth = get_depth(assignment.name, scopes)


@multimethod
def resolve(lox_super: Super, scopes: deque):
    lox_super.depth = get_depth("super", scopes)


@multimethod
def resolve(call: Call, scopes: deque):
    resolve(call.callee, scopes)
    for arg in call.arguments:
        resolve(arg, scopes)


@multimethod
def resolve(stmt: ExprStmt, scopes: deque):
    resolve(stmt.expression, scopes)


@multimethod
def resolve(_: Literal, __: deque):
    pass


@multimethod
def resolve(expr: Unary, scopes: deque):
    resolve(expr.right, scopes)


@multimethod
def resolve(expr: Binary, scopes: deque):
    resolve(expr.left, scopes)
    resolve(expr.right, scopes)


@multimethod
def resolve(expr: Grouping, scopes: deque):
    resolve(expr.expression, scopes)


@multimethod
def resolve(expr: Logical, scopes: deque):
    resolve(expr.left, scopes)
    resolve(expr.right, scopes)


@multimethod
def resolve(this: This, scopes: deque):
    this.depth = get_depth("this", scopes)


@multimethod
def resolve(fun: AnonymousFun, scopes: deque):
    start_scope(scopes)
    for param in fun.params:
        declare(param, scopes)
        define(param, scopes)
    resolve(fun.body, scopes)
    end_scope(scopes)


@multimethod
def resolve(expr: LoxGet, scopes: deque):
    resolve(expr.obj, scopes)


@multimethod
def resolve(expr: LoxSet, scopes: deque):
    resolve(expr.obj, scopes)
    resolve(expr.val, scopes)


@multimethod
def resolve(var: VarStmt, scopes: deque):
    declare(var.name, scopes)
    if var.initializer:
        resolve(var.initializer, scopes)
    define(var.name, scopes)


@multimethod
def resolve(block: BlockStmt, scopes: deque):
    start_scope(scopes)
    for statement in block.statements:
        resolve(statement, scopes)
    end_scope(scopes)


@multimethod
def resolve(function: FunctionStmt, scopes: deque):
    declare(function.name, scopes)
    define(function.name, scopes)

    start_scope(scopes)
    for token in function.params:
        declare(token, scopes)
        define(token, scopes)
    resolve(function.body, scopes)
    end_scope(scopes)


@multimethod
def resolve(stmt: PrintStmt, scopes: deque):
    resolve(stmt.expression, scopes)


@multimethod
def resolve(stmt: IfStmt, scopes: deque):
    resolve(stmt.condition, scopes)
    resolve(stmt.then_branch, scopes)
    if stmt.else_branch:
        resolve(stmt.else_branch, scopes)


@multimethod
def resolve(stmt: WhileStmt, scopes: deque):
    resolve(stmt.condition, scopes)
    resolve(stmt.body, scopes)


@multimethod
def resolve(stmt: ReturnStmt, scopes: deque):
    resolve(stmt.value, scopes)


@multimethod
def resolve(stmt: ClassStmt, scopes: deque):
    declare(stmt.name, scopes)
    define(stmt.name, scopes)

    if stmt.superclass:
        resolve(stmt.superclass, scopes)
        start_scope(scopes)
        scopes[0]["super"] = True

    start_scope(scopes)
    scopes[0]["this"] = True
    for method in stmt.methods:
        resolve(method, scopes)
    end_scope(scopes)

    if stmt.superclass:
        end_scope(scopes)


def resolve_statements(statements: List[Stmt]):
    scopes = deque()
    for statement in statements:
        resolve(statement, scopes)



