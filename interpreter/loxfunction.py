from ast.stmt import FunctionStmt
from environment.environment import Environment
from ast.lox_callable import LoxCallable


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt):
        self.declaration = declaration
        self._arity = len(declaration.params)

    def arity(self):
        return self._arity

    def call(self, closure: Environment, *args):
        from interpreter.execute_stmt import execute_stmt
        env = Environment()
        env.outer_env = closure
        for param_position, param in enumerate(self.declaration.params):
            env.define(param.lexeme, args[param_position])
        execute_stmt(self.declaration.body, env)
