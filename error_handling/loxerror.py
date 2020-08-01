from scanner.token import Token


class LoxError(Exception):
    pass


class LoxParseError(LoxError):
    def __init__(self, msg: str, token: Token):
        self.msg = msg
        self.token = token


class LoxRuntimeError(LoxError):
    def __init__(self, msg: str, token: Token = None):
        self.msg = msg
        self.token = token
