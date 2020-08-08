from multimethod.multimethod import multimethod
from scanner.tokentypes import TokenType
from error_handling.loxerror import LoxRuntimeError
from environment.environment import Environment
from ast.expr import *
from interpreter.validations import is_numeric, is_string


@multimethod
def execute_expr(literal: Literal, _: Environment = None):
    return literal.value


@multimethod
def execute_expr(unary: Unary, env: Environment):
    right = execute_expr(unary.right, env)
    operator = unary.operator.lexeme
    if operator == "!":
        return not right
    elif operator == "-":
        if not is_numeric(right):
            raise LoxRuntimeError("Invalid operand for unary -")
        else:
            return -right
    raise LoxRuntimeError("Invalid operator found for unary")


@multimethod
def execute_expr(binary: Binary, env: Environment):
    left = execute_expr(binary.left, env)
    right = execute_expr(binary.right, env)

    validation_logic = {
        TokenType.SLASH: lambda: is_numeric(left) and is_numeric(right),
        TokenType.STAR: lambda: is_numeric(left) and is_numeric(right),
        TokenType.PLUS: lambda: (is_numeric(left) and is_numeric(right)) or (is_string(left) and is_string(right)),
        TokenType.MINUS: lambda: is_numeric(left) and is_numeric(right),
        TokenType.BANG_EQUAL: lambda: True,
        TokenType.EQUAL_EQUAL: lambda: True,
        TokenType.GREATER: lambda: is_numeric(left) and is_numeric(right),
        TokenType.GREATER_EQUAL: lambda: is_numeric(left) and is_numeric(right),
        TokenType.LESS: lambda: is_numeric(left) and is_numeric(right),
        TokenType.LESS_EQUAL: lambda: is_numeric(left) and is_numeric(right),
    }

    execution_logic = {
        TokenType.SLASH: lambda: left / right,
        TokenType.STAR: lambda: left * right,
        TokenType.PLUS: lambda: left + right,
        TokenType.MINUS: lambda: left - right,
        TokenType.BANG_EQUAL: lambda: left != right,
        TokenType.EQUAL_EQUAL: lambda: left == right,
        TokenType.GREATER: lambda: left > right,
        TokenType.GREATER_EQUAL: lambda: left >= right,
        TokenType.LESS: lambda: left < right,
        TokenType.LESS_EQUAL: lambda: left <= right,
    }

    if binary.operator.tokentype not in validation_logic or not validation_logic[binary.operator.tokentype]():
        raise LoxRuntimeError("Invalid binary operands, must be two numbers or two strings")
    return execution_logic[binary.operator.tokentype]()


@multimethod
def execute_expr(grouping: Grouping, env: Environment):
    return execute_expr(grouping.expression, env)


@multimethod
def execute_expr(variable: Variable, env: Environment):
    return env.get(variable.var, variable.depth)


@multimethod
def execute_expr(this: This, env: Environment):
    return env.get(this.this, this.depth)

@multimethod
def execute_expr(assignment: Assign, env: Environment):
    return env.assign(assignment.var.var, execute_expr(assignment.val, env), assignment.var.depth)


@multimethod
def execute_expr(logical: Logical, env: Environment):
    left = execute_expr(logical.left, env)
    if logical.operator.is_token_type([TokenType.OR]):
        if left:
            return left
    elif not left:
        return left

    return execute_expr(logical.right, env)


@multimethod
def execute_expr(call: Call, env: Environment):
    from ast.lox_callable import LoxCallable
    callee = execute_expr(call.callee, env)
    if not issubclass(type(callee), LoxCallable):
        raise LoxRuntimeError("Invalid callee")
    if len(call.arguments) != callee.arity():
        raise LoxRuntimeError("Invalid number of arguments", call.paren)
    args = []
    for arg in call.arguments:
        args.append(execute_expr(arg, env))
    return callee.call(*list(args))


@multimethod
def execute_expr(fun: AnonymousFun, env: Environment):
    from interpreter.loxfunction import LoxFunction
    return LoxFunction(fun, env)


@multimethod
def execute_expr(lox_get: LoxGet, env: Environment):
    obj = execute_expr(lox_get.obj, env)
    return obj.get(lox_get.name)


@multimethod
def execute_expr(lox_set: LoxSet, env: Environment):
    obj = execute_expr(lox_set.obj, env)
    return obj.set(lox_set.name, execute_expr(lox_set.val, env))



