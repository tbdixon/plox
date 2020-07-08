from scanner.token import Token

class Error(Exception):
    pass


class ParseError(Error):
    def __init__(self, msg: str, token: Token = None):
        self.msg = msg
        self.token = token
