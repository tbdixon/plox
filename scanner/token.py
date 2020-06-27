from .tokentypes import TokenType

class Token:
    def __init__(self, tokentype: TokenType, lexeme: str , literal, line: int) -> None:
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f'Type: {self.tokentype} Lexeme: {self.lexeme} Literal: {self.literal} Line {self.line}'
