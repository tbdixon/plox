import sys
from scanner.scanner import Scanner
from parser.parser import Parser
from ast.ast_printer import ast_print
from ast.ast_execute import ast_execute
from ast.expr import InvalidExpr
from error_handling.error_printer import parser_error_print


def run_prompt() -> None:
    while True:
        line = input("> ")
        if line is not None:
            # Handle ctrl-c etc in a clean manner
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
        print(ast_execute(ast))


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
