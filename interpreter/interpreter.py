from typing import List

from interpreter.execute_stmt import execute_stmt

from ast.stmt import Stmt


class Interpreter:
    def __init__(self, statements: List[Stmt]):
        self.statements = statements

    def interpret(self) -> None:
        for statement in self.statements:
            execute_stmt(statement)
