from scanner.token import Token
from error_handling.loxerror import LoxRuntimeError


class Environment:
    def __init__(self):
        self.outer_env = None
        self.values = dict()

    def define(self, name: str, val):
        self.values[name] = val

    def assign(self, name: Token, val):
        if name.lexeme in self.values:
            self.values[name.lexeme] = val
            return val
        elif self.outer_env:
            return self.outer_env.assign(name, val)
        raise LoxRuntimeError(f'Undefined variable {name.lexeme}')

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.outer_env:
            return self.outer_env.get(name)
        raise LoxRuntimeError(f'Undefined variable {name.lexeme}')
