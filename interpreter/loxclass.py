from typing import Dict

from scanner.token import Token
from ast.lox_callable import LoxCallable
from error_handling.loxerror import LoxRuntimeError


class LoxClass(LoxCallable):
    def __init__(self, name: Token, methods: Dict):
        self.name = name
        self.methods = methods

    def call(self, *args):
        return LoxInstance(self)

    def arity(self):
        return 0

    def getMethod(self, name: Token):
        return self.methods[name.lexeme]

    def __str__(self):
        return self.name.lexeme


class LoxInstance:
    def __init__(self, lox_class: LoxClass):
        self.lox_class = lox_class
        self.fields = {}

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        elif name.lexeme in self.lox_class.methods:
            method = self.lox_class.getMethod(name)
            return method.bind(self)
        raise LoxRuntimeError("Invalid field ", name)

    def set(self, name: Token, val):
        self.fields[name.lexeme] = val
        return val

    def __str__(self):
        return self.lox_class.name.lexeme + " instance"
