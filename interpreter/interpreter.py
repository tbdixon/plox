from typing import List

import time

from environment.environment import Environment

from ast.stmt import Stmt

from ast.lox_callable import LoxCallable


# native function sample
class Clock(LoxCallable):
    def __init__(self):
        pass

    def arity(self) -> int:
        return 0

    def call(self, env, *args):
        return time.time()

    def __str__(self):
        return "<native fn>"


class Interpreter:
    def __init__(self):
        self.environment = self.globals = Environment()
        self.globals.define('clock', Clock())

    def interpret(self, statements: List[Stmt]) -> None:
        from interpreter.execute_stmt import execute_stmt
        for statement in statements:
            execute_stmt(statement, self.environment)
