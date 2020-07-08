from .token import Token
from .tokentypes import TokenType
from error_handling.error_printer import scanner_error_print


class Scanner:
    # TODO: this should probably be paired up as a map with the type enum
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

    single_tokens = {
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        "-": TokenType.MINUS,
        "+": TokenType.PLUS,
        ";": TokenType.SEMICOLON,
        "*": TokenType.STAR
    }

    double_tokens = {
        "!": TokenType.BANG,
        "!=": TokenType.BANG_EQUAL,
        "=": TokenType.EQUAL,
        "==": TokenType.EQUAL_EQUAL,
        ">": TokenType.GREATER,
        ">=": TokenType.GREATER_EQUAL,
        "<": TokenType.LESS,
        "<=": TokenType.LESS_EQUAL
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.source_lines = source.split("\n")
        self.tokens = list()
        self.start = self.current = 0
        self.line_num = 1
        self.had_error = False
        self.scan_funcs = {
            " ": lambda _: None,
            "\r": lambda _: None,
            '\t': lambda _: None,
            "\n": self.scan_newline,
            "/": self.scan_slash,
            "\"": self.parse_string,
        }
        for t in self.single_tokens:
            self.scan_funcs[t] = self.scan_single_token
        for t in self.double_tokens:
            self.scan_funcs[t] = self.scan_double_token


    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self) -> str:
        # Return the current character and advance current
        self.current = self.current + 1
        return self.source[self.current - 1]

    def preview_next(self) -> str:
        return self.source[self.current:self.current + 1]

    def eat_line(self) -> None:
        # Consume (and throw away) the rest of the current line
        while not self.is_at_end() and self.source[self.current] != '\n':
            self.current = self.current + 1
        self.current = self.current + 1
        self.line_num = self.line_num + 1

    def scan_newline(self, _: str):
        self.line_num = self.line_num + 1

    def scan_single_token(self, c: str) -> None:
        self.tokens.append(Token(self.single_tokens[c], c, None, self.line_num))

    def scan_double_token(self, c: str) -> None:
        if self.preview_next() == "=":
            c = c + self.advance()
        self.tokens.append(Token(self.double_tokens[c], c, None, self.line_num))

    def scan_slash(self, _: str) -> None:
        if self.preview_next() == "/":
            self.eat_line()
        else:
            self.tokens.append(Token(TokenType.SLASH, "/", None, self.line_num))

    def parse_word(self, initial_char: str) -> None:
        word = initial_char
        while not self.is_at_end():
            if self.preview_next() == "\n" or self.preview_next() == " " or not self.preview_next().isalpha():
                break
            else:
                word = word + self.advance()
        if word in self.keywords:
            self.tokens.append(Token(self.keywords[word], word, None, self.line_num))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, word, None, self.line_num))

    def parse_number(self, initial_char: str) -> None:
        # TODO: Deal with trailing decimals and make this look less terrible.
        number = initial_char
        decimal_seen = False
        decimal_error = False
        while not self.is_at_end():
            if self.preview_next() == ".":
                if decimal_seen:
                    # Can't have two decimals in a single number
                    decimal_error = True
                    self.had_error = True
                    scanner_error_print("Invalid number", self.line_num, self.source_lines[self.line_num - 1])
                    number = number + self.advance()
                else:
                    decimal_seen = True
                    number = number + self.advance()
            elif self.preview_next() == "\n" or self.preview_next() == " " or not self.preview_next().isnumeric():
                break
            else:
                number = number + self.advance()
        if not decimal_error:
            number = float(number) if decimal_seen else int(number)
        self.tokens.append(Token(TokenType.NUMBER, self.get_lexeme(), number, self.line_num))

    def parse_string(self, _: str) -> None:
        output = ""
        while not self.is_at_end():
            if self.preview_next() == '"':
                # Grab the closing quote
                self.advance()
                self.tokens.append(Token(TokenType.STRING, self.get_lexeme(), output, self.line_num))
                return
            else:
                output = output + self.advance()
        # If we don't hit the closing quote, we have an error
        self.had_error = True
        scanner_error_print("Reached EOF in string", self.line_num, self.source_lines[self.line_num - 1])

    def get_lexeme(self) -> str:
        return self.source[self.start:self.current]

    def scan_tokens(self) -> None:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line_num))

    def scan_token(self) -> None:
        current_char = self.advance()
        if current_char in self.scan_funcs:
            self.scan_funcs[current_char](current_char)
            return
        # Numbers
        elif current_char.isnumeric():
            self.parse_number(current_char)
            return
        # Identifiers and Keywords
        elif current_char.isalpha():
            self.parse_word(current_char)
            return
        else:
            self.had_error = True
            scanner_error_print("Invalid character", self.line_num, self.source_lines[self.line_num - 1])
