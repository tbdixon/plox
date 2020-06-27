from .token import Token
from .tokentypes import TokenType
from error_handler.error_handler import plox_error


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.source_lines = source.split("\n")
        self.tokens = list()
        self.start = self.current = 0
        self.line_num = 1
        self.had_error = False

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self) -> str:
        # Return the current character and advance current
        self.current = self.current + 1
        return self.source[self.current - 1]

    def eat_line(self) -> None:
        while not self.is_at_end() and self.source[self.current] != '\n':
            self.current = self.current + 1
            pass
        self.current = self.current + 1
        self.line_num = self.line_num + 1

    def preview_next(self) -> str:
        return self.source[self.current:self.current + 1]

    def scan_tokens(self) -> None:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line_num))

    def scan_token(self) -> None:
        current_char = self.advance()
        # Ignore whitespace
        if current_char == " " or current_char == '\r' or current_char == '\t':
            return
        # Ignore newlines except to increment current line_num
        elif current_char == "\n":
            self.line_num = self.line_num + 1
            return
        elif current_char == "(":
            self.tokens.append(Token(TokenType.LEFT_PAREN, "(", None, self.line_num))
            return
        elif current_char == ")":
            self.tokens.append(Token(TokenType.RIGHT_PAREN, ")", None, self.line_num))
            return
        elif current_char == "{":
            self.tokens.append(Token(TokenType.LEFT_BRACE, "{", None, self.line_num))
            return
        elif current_char == "}":
            self.tokens.append(Token(TokenType.RIGHT_BRACE, "}", None, self.line_num))
            return
        elif current_char == ",":
            self.tokens.append(Token(TokenType.COMMA, ",", None, self.line_num))
            return
        elif current_char == ".":
            self.tokens.append(Token(TokenType.DOT, ".", None, self.line_num))
            return
        elif current_char == "-":
            self.tokens.append(Token(TokenType.MINUS, "-", None, self.line_num))
            return
        elif current_char == "+":
            self.tokens.append(Token(TokenType.PLUS, "+", None, self.line_num))
            return
        elif current_char == ";":
            self.tokens.append(Token(TokenType.SEMICOLON, ";", None, self.line_num))
            return
        elif current_char == "*":
            self.tokens.append(Token(TokenType.STAR, "*", None, self.line_num))
            return
        elif current_char == "/" and self.preview_next() != "/":
            self.tokens.append(Token(TokenType.SLASH, "/", None, self.line_num))
            return
        elif current_char == "/" and self.preview_next() == "/":
            self.eat_line()
            return
        else:
            self.had_error = True
            plox_error("Invalid character", self.line_num, self.source_lines[self.line_num - 1])
