from scanner.token import Token
from error_handling.loxerror import LoxRuntimeError


class LoxReturn(Exception):
    def __init__(self, ret_val):
        self.ret_val = ret_val


class Environment:
    def __init__(self, outer_env = None):
        self.outer_env = outer_env
        self.values = dict()

    def define(self, name: str, val):
        self.values[name] = val

    def assign(self, name: Token, val, depth):
        if depth == 0:
            if name.lexeme in self.values:
                self.values[name.lexeme] = val
                return val
            raise LoxRuntimeError(f'Undefined assignment variable {name.lexeme}')
        else:
            return self.outer_env.assign(name, val, depth - 1)

    def get(self, name: str, depth: int):
        if depth == 0:
            if name in self.values:
                return self.values[name]
            raise LoxRuntimeError(f'Undefined get variable {name}')
        else:
            return self.outer_env.get(name, depth - 1)
