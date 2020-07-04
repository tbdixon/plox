from ast.ast_printer import ast_print
from ast.expr import *
from scanner.token import Token
from scanner.tokentypes import TokenType

if __name__ == '__main__':
    expression = Binary(Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)), Token(TokenType.STAR, "*", None, 1),
                        Grouping(Literal(45.67)))
    print(ast_print(expression))
