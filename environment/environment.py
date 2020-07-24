from scanner.token import Token
from error_handling.loxerror import LoxRuntimeError
class Environment:
    def __init__(self):
        self.values = dict()

    def define(self, name: str, val):
        self.values[name] = val

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise LoxRuntimeError(f'Undefined variable {name.lexeme}')

