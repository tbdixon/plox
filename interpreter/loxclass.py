from typing import Dict, Union

from scanner.token import Token
from ast.lox_callable import LoxCallable
from error_handling.loxerror import LoxRuntimeError


class LoxClass(LoxCallable):
    def __init__(self, name: Token, superclass: 'LoxClass', methods: Dict):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def call(self, *args):
        instance = LoxInstance(self)
        if "init" in self.methods:
            instance.init(*args)
        return instance

    def arity(self):
        return self.methods["init"].arity() if "init" in self.methods else 0

    def getMethod(self, name: Token):
        if name.lexeme in self.methods:
            return self.methods[name.lexeme]
        elif self.superclass:
            return self.superclass.getMethod(name)
        raise LoxRuntimeError("Invalid field ", name)

    def __str__(self):
        return self.name.lexeme


class LoxInstance:
    def __init__(self, lox_class: LoxClass):
        self.lox_class = lox_class
        self.fields = {}

    def init(self, *args):
        init = self.lox_class.methods["init"]
        init.bind(self).call(*args)
        return self

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        else:
            method = self.lox_class.getMethod(name)
            return method.bind(self)

    def set(self, name: Token, val):
        self.fields[name.lexeme] = val
        return val

    def __str__(self):
        return self.lox_class.name.lexeme + " instance"
