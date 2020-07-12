import sys
from scanner.scanner import Scanner
from parser.parser import Parser
from ast.ast_printer import ast_print
from ast.ast_execute import ast_execute
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
            run(line)


def run_file(filename: str) -> None:
    script = open(filename, 'r').read()
    print(f'executing {filename}')
    run(script)


def run(source: str) -> None:
    s = Scanner(source)
    s.scan_tokens()

    p = Parser(s.tokens)
    ast = p.parse()

    if type(ast) == InvalidExpr:
        parser_error_print(ast.error, s.source_lines)
    else:
        print(ast_print(ast))
        try:
            print(ast_execute(ast))
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
