class LoxError(Exception):
    pass


class LoxParseError(LoxError):
    def __init__(self, msg: str, token):
        self.msg = msg
        self.token = token


class LoxRuntimeError(LoxError):
    def __init__(self, msg: str):
        self.msg = msg
