from .expr import *
from multimethod.multimethod import multimethod


@multimethod
def ast_print(literal: Literal) -> str:
    if literal.value:
        return str(literal.value)
    else:
        return "Nil"


@multimethod
def ast_print(unary: Unary) -> str:
    return parenthesize(unary.operator.lexeme, unary.right)


@multimethod
def ast_print(binary: Binary) -> str:
    return parenthesize(binary.operator.lexeme, binary.left, binary.right)


@multimethod
def ast_print(grouping: Grouping) -> str:
    return parenthesize("group ()", grouping.expression)


def parenthesize(val: str, *exprs):
    output = list()
    output.append(f'( {val}')
    for expr in exprs:
        output.append(" ")
        output.append(ast_print(expr))
    output.append(")")
    return "".join(output)
