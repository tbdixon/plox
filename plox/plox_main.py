import sys
from .scanner import scanner, token

HAD_ERROR = False


def plox_error(line_num: int, line: str) -> None:
    global HAD_ERROR
    HAD_ERROR = True
    print(f'Error on line {line_num} {line} ')


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
    scanner(source)
    scanner.scan_tokens()
    for t in scanner.tokens:
        # if HAD_ERROR...
        print(t)


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
