from typing import List

from interpreter.execute_stmt import execute_stmt

from environment.environment import Environment

from ast.stmt import Stmt


class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements: List[Stmt]) -> None:
        for statement in statements:
            execute_stmt(statement, self.environment)
