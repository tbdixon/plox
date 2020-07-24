from typing import List

from .loxerror import LoxParseError


def scanner_error_print(msg: str, line_num: int, line: str) -> None:
    print(f'{msg} on line {line_num}\n  >>>>  {line} ')


def parser_error_print(error: LoxParseError, source: List[str]) -> None:
    print(f'{error.msg}\nLine {error.token.line}: {source[error.token.line - 1]} ')
