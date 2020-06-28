from .token import Token
from .tokentypes import TokenType
from error_handler.error_handler import plox_error


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "fun": TokenType.FUN,
        "for": TokenType.FOR,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

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
        self.current = self.current + 1
        self.line_num = self.line_num + 1

    def preview_next(self) -> str:
        return self.source[self.current:self.current + 1]

    def parse_word(self, initial_char: str) -> str:
        word = initial_char
        while not self.is_at_end():
            if self.preview_next() == "\n" or self.preview_next() == " " or not self.preview_next().isalpha():
                return word
            else:
                word = word + self.advance()
        return word

    def parse_number(self, initial_char: str) -> str:
        # TODO: Deal with trailing decimals
        number = initial_char
        decimal_seen = False
        while not self.is_at_end():
            if self.preview_next() == ".":
                if decimal_seen:
                    # Can't have two decimals in a single number
                    self.had_error = True
                    plox_error("Invalid number", self.line_num, self.source_lines[self.line_num - 1])
                else:
                    decimal_seen = True
                    number = number + self.advance()
            elif self.preview_next() == "\n" or self.preview_next() == " " or not self.preview_next().isnumeric():
                break
            else:
                number = number + self.advance()
        return float(number) if decimal_seen else int(number)

    def parse_string(self) -> str:
        string = ""
        while not self.is_at_end():
            if self.preview_next() != '"':
                string = string + self.advance()
            else:
                self.advance()
                return string
        # If we don't hit the closing quote, we have an error
        self.had_error = True
        plox_error("Reached EOF in string", self.line_num, self.source_lines[self.line_num - 1])

    def get_lexeme(self) -> str:
        return self.source[self.start:self.current]

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
        # Simple single character tokens
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
        # Comment vs Slash
        elif current_char == "/":
            if self.preview_next() != "/":
                self.tokens.append(Token(TokenType.SLASH, "/", None, self.line_num))
            else:
                self.eat_line()
            return
        # One or two character tokens
        elif current_char == "!":
            if self.preview_next() == "=":
                self.advance()
                self.tokens.append(Token(TokenType.BANG_EQUAL, "!=", None, self.line_num))
            else:
                self.tokens.append(Token(TokenType.BANG, "!", None, self.line_num))
            return
        elif current_char == "=":
            if self.preview_next() == "=":
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL_EQUAL, "==", None, self.line_num))
            else:
                self.tokens.append(Token(TokenType.EQUAL, "=", None, self.line_num))
            return
        elif current_char == ">":
            if self.preview_next() == "=":
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, ">=", None, self.line_num))
            else:
                self.tokens.append(Token(TokenType.GREATER, ">", None, self.line_num))
            return
        elif current_char == "<":
            if self.preview_next() == "=":
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, "<=", None, self.line_num))
            else:
                self.tokens.append(Token(TokenType.LESS, "<", None, self.line_num))
            return
        # Strings
        elif current_char == '"':
            string = self.parse_string()
            self.tokens.append(Token(TokenType.STRING, self.get_lexeme(), string, self.line_num))
            return
        # Numbers
        elif current_char.isnumeric():
            number = self.parse_number(current_char)
            self.tokens.append(Token(TokenType.NUMBER, self.get_lexeme(), number, self.line_num))
            return
        # Identifiers and Keywords
        elif current_char.isalpha():
            word = self.parse_word(current_char)
            if word in self.keywords:
                self.tokens.append(Token(self.keywords[word], word, None, self.line_num))
            else:
                self.tokens.append(Token(TokenType.IDENTIFIER, word, None, self.line_num))
            return
        else:
            self.had_error = True
            plox_error("Invalid character", self.line_num, self.source_lines[self.line_num - 1])
            return
