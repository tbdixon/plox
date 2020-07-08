from typing import List

from .error import ParseError


def scanner_error_print(msg: str, line_num: int, line: str) -> None:
    print(f'{msg} on line {line_num}\n  >>>>  {line} ')


def parser_error_print(error: ParseError, source: List[str]) -> None:
    print(f'{error.msg} on {error.token}\nLine {error.token.line}: {source[error.token.line - 1]} ')
