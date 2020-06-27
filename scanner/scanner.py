from .token import Token
from .tokentypes import TokenType
from plox_main import plox_error

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = list()
        self.start = self.current = 0
        self.line_num = 1
        #self.line = ""
        print("Scanning")

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_tokens(self) -> None:
        #self.line = self.source[self.current:]
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line_num))

    def advance(self) -> str:
        self.current = self.current + 1
        return self.source[self.current - 1]

    def scan_token(self) -> None:
        current_char = self.advance()
        if current_char == "\n":
            self.line_num = self.line_num + 1
        elif current_char == "(":
            self.tokens.append(Token(TokenType.LEFT_PAREN, "(", None, self.line_num))
        elif current_char == ")":
            self.tokens.append(Token(TokenType.RIGHT_PAREN, ")", None, self.line_num))
        elif current_char == "{":
            self.tokens.append(Token(TokenType.LEFT_BRACE, "{", None, self.line_num))
        elif current_char == "}":
            self.tokens.append(Token(TokenType.RIGHT_BRACE, "}", None, self.line_num))
        elif current_char == ",":
            self.tokens.append(Token(TokenType.COMMA, ",", None, self.line_num))
        elif current_char == ".":
            self.tokens.append(Token(TokenType.DOT, ".", None, self.line_num))
        elif current_char == "-":
            self.tokens.append(Token(TokenType.MINUS, "-", None, self.line_num))
        elif current_char == "+":
            self.tokens.append(Token(TokenType.PLUS, "+", None, self.line_num))
        elif current_char == ";":
            self.tokens.append(Token(TokenType.SEMICOLON, ";", None, self.line_num))
        elif current_char == "/":
            self.tokens.append(Token(TokenType.SLASH, "/", None, self.line_num))
        elif current_char == "*":
            self.tokens.append(Token(TokenType.STAR, "*", None, self.line_num))
        else:
            plox_error(self.line_num, current_char)