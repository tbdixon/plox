from multimethod.multimethod import multimethod
from scanner.tokentypes import TokenType
from error_handling.loxerror import LoxRuntimeError
from ast.expr import *
from ast.validations import is_numeric, is_string


@multimethod
def execute_expr(literal: Literal):
    return literal.value


@multimethod
def execute_expr(unary: Unary):
    right = execute_expr(unary.right)
    operator = unary.operator.lexeme
    if operator == "!":
        return not right
    elif operator == "-":
        if not is_numeric(right):
            raise LoxRuntimeError("Invalid operand for unary -", unary)
        else:
            return -right
    raise LoxRuntimeError("Invalid operator found for unary", unary)


@multimethod
def execute_expr(binary: Binary):
    left = execute_expr(binary.left)
    right = execute_expr(binary.right)

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
        raise LoxRuntimeError("Invalid binary operands, must be two numbers or two strings", binary)
    return execution_logic[binary.operator.tokentype]()


@multimethod
def execute_expr(grouping: Grouping):
    return execute_expr(grouping.expression)