import sys
from scanner.scanner import Scanner
from parser.parser import Parser
from interpreter.execute_expr import execute_expr
from interpreter.interpreter import Interpreter
from ast.expr import InvalidExpr
from error_handling.error_printer import parser_error_print
from error_handling.loxerror import LoxRuntimeError


def run_prompt() -> None:
    while True:
        try:
            line = input("> ")
        # Probably better to use signals for SIGINT, but this is quick and easy for now
        except (EOFError, KeyboardInterrupt) as err:
            if isinstance(err, EOFError):
                sys.exit(0)
            else:
                print("\n")
                continue
        if len(line):
            # if line[-1] != ";":
            #    line.append(";")
            run(line)


def run_file(filename: str) -> None:
    script = open(filename, 'r').read()
    print(f'executing {filename}')
    run(script)


def run(source: str) -> None:
    scanner = Scanner(source)
    scanner.scan_tokens()

    parser = Parser(scanner.tokens)
    statements = parser.parse()

    if parser.had_error:
        print(f'Error parsing...')

    interpreter = Interpreter(statements)
    try:
        interpreter.interpret()
    except LoxRuntimeError as err:
        print(f'{err.msg}: {err.expr}')


def main():
    args = sys.argv[1:]
    if len(args) > 1:
        print(f'Usage: plox [script]')
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_prompt()


if __name__ == '__main__':
    main()
