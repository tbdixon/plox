from multimethod.multimethod import multimethod
from scanner.tokentypes import TokenType
from .expr import *


@multimethod
def ast_execute(literal: Literal):
    return literal.value


@multimethod
def ast_execute(unary: Unary):
    right = ast_execute(unary.right)
    operator = unary.operator.lexeme
    if operator == "!":
        return not right
    if operator == "-":
        return -right
    # TODO: error handling here and everywhere...


@multimethod
def ast_execute(binary: Binary):
    left = ast_execute(binary.left)
    right = ast_execute(binary.right)

    execution_logic = {
        TokenType.SLASH: lambda: left/right,
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

    if binary.operator.tokentype in execution_logic:
        return execution_logic[binary.operator.tokentype]()
    else:
        #error time
        pass

@multimethod
def ast_execute(grouping: Grouping):
    return ast_execute(grouping.expression)