from .expr import *


def print_literal(literal: Literal) -> str:
    if literal.value:
        return str(literal.value)
    else:
        return "Nil"


def print_unary(unary: Unary) -> str:
    return parenthesize(unary.operator.lexeme, unary.right)


def print_binary(binary: Binary) -> str:
    return parenthesize(binary.operator.lexeme, binary.left, binary.right)


def print_grouping(grouping: Grouping) -> str:
    return parenthesize("group ()", grouping.expression)


def parenthesize(val: str, *exprs):
    output = list()
    output.append(f'( {val}')
    for expr in exprs:
        output.append(" ")
        output.append(ast_print(expr))
    output.append(")")
    return "".join(output)


printers = {
    "Literal": print_literal,
    "Unary": print_unary,
    "Binary": print_binary,
    "Grouping": print_grouping
}


def ast_print(expression: Expr) -> str:
    return printers[type(expression).__name__](expression)
