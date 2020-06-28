from .tokentypes import TokenType


class Token:
    def __init__(self, tokentype: TokenType, lexeme: str, literal, line: int) -> None:
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        else:
            return self.tokentype == other.tokentype and self.lexeme == other.lexeme and self.literal == other.literal and self.line == other.line

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f'Type: {self.tokentype} Lexeme: {self.lexeme} Literal: {self.literal} Line {self.line}'
        # Useful to generate code for test output...
        # return f'self.expected_tokens.append(Token({self.tokentype}, "{self.lexeme}", {self.literal}, {self.line}))'
