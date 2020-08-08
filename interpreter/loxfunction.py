from typing import Union

from ast.stmt import FunctionStmt
from ast.expr import AnonymousFun
from environment.environment import Environment, LoxReturn
from ast.lox_callable import LoxCallable

from enum import Enum, auto


class FunctionType(Enum):
    # Single character tokens
    NONE = auto()
    FUNCTION = auto()
    METHOD = auto()


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Union[FunctionStmt, AnonymousFun], closure: Environment, function_type: FunctionType = FunctionType.NONE):
        self.declaration = declaration
        self.closure = closure
        self.function_type = function_type
        self._arity = len(declaration.params)

    def arity(self):
        return self._arity

    def bind(self, this):
        env = Environment()
        env.outer_env = self.closure
        env.define("this", this)
        return LoxFunction(self.declaration, env)

    def call(self, *args):
        from interpreter.execute_stmt import execute_stmt
        env = Environment()
        env.outer_env = self.closure
        for param_position, param in enumerate(self.declaration.params):
            env.define(param.lexeme, args[param_position])
        try:
            execute_stmt(self.declaration.body, env)
        except LoxReturn as ret:
            return ret.ret_val
        return None
