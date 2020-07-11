
class LoxError(Exception):
    pass


class LoxParseError(LoxError):
    def __init__(self, msg: str, token = None):
        self.msg = msg
        self.token = token


class LoxRuntimeError(LoxError):
    def __init__(self, msg: str, expr = None):
        self.msg = msg
        self.expr = expr