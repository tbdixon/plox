from multimethod.multimethod import multimethod
from scanner.tokentypes import TokenType
from error_handling.loxerror import LoxRuntimeError
from .expr import *
from .validations import is_numeric, is_string


@multimethod
def ast_execute(literal: Literal):
    return literal.value


@multimethod
def ast_execute(unary: Unary):
    right = ast_execute(unary.right)
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
def ast_execute(binary: Binary):
    left = ast_execute(binary.left)
    right = ast_execute(binary.right)

    validation_logic = {
        TokenType.SLASH: lambda: is_numeric(left) and is_numeric(right),
        TokenType.STAR: lambda: is_numeric(left) and is_numeric(right),
        TokenType.PLUS: lambda: (is_numeric(left) and is_numeric(right)) or (is_string(left) and is_string(right)),
        TokenType.MINUS: lambda: is_numeric(left) and is_numeric(right),
        TokenType.BANG_EQUAL: lambda: True,
        TokenType.EQUAL_EQUAL: lambda: True,
        TokenType.GREATER: lambda: True,
        TokenType.GREATER_EQUAL: lambda: True,
        TokenType.LESS: lambda: True,
        TokenType.LESS_EQUAL: lambda: True,
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

    if binary.operator.tokentype not in validation_logic or not validation_logic[binary.operator.tokentype]:
        raise LoxRuntimeError("Invalid token", binary)
    return execution_logic[binary.operator.tokentype]()


@multimethod
def ast_execute(grouping: Grouping):
    return ast_execute(grouping.expression)