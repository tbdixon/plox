import unittest
from scanner.scanner import Scanner, Token, TokenType


class TestScannerUtils(unittest.TestCase):
    def setUp(self):
        self.source = "Hello\nWorld"
        self.scanner = Scanner(self.source)

    def test_is_at_end(self):
        self.scanner.current = 0
        self.assertFalse(self.scanner.is_at_end())
        self.scanner.current = len(self.source)
        self.assertTrue(self.scanner.is_at_end())

    def test_advance(self):
        c = self.scanner.advance()
        self.assertEqual(c, "H")
        self.assertEqual(self.scanner.current, 1)

    def test_preview_next(self):
        self.assertEqual(self.scanner.preview_next(), "H")
        self.assertEqual(self.scanner.current, 0)
        self.scanner.current = 5
        self.assertEqual(self.scanner.preview_next(), self.source[5])
        self.assertEqual(self.scanner.current, 5)
        self.scanner.current = len(self.source)
        self.assertEqual('', self.scanner.preview_next())
        self.assertEqual(self.scanner.current, len(self.source))

    def test_eat_line(self):
        self.scanner.eat_line()
        self.assertEqual(self.scanner.line_num, 2)
        self.assertEqual(self.scanner.current, 6)
        self.scanner.eat_line()
        self.assertEqual(self.scanner.line_num, 3)
        self.assertTrue(self.scanner.is_at_end())

    def test_parse_word(self):
        self.scanner.source = "First\nSecond Third while"
        c = self.scanner.advance()
        self.assertEqual(self.scanner.parse_word(c), Token(TokenType.IDENTIFIER, "First", None, 1))
        # Simulate the second iteration eating the \n
        self.scanner.advance()
        c = self.scanner.advance()
        self.assertEqual(self.scanner.parse_word(c), Token(TokenType.IDENTIFIER, "Second", None, 2))
        self.scanner.advance()
        c = self.scanner.advance()
        self.assertEqual(self.scanner.parse_word(c), Token(TokenType.IDENTIFIER, "Third", None, 2))
        self.scanner.advance()
        c = self.scanner.advance()
        self.assertEqual(self.scanner.parse_word(c), Token(TokenType.WHILE, "while", None, 2))

    def test_parse_number(self):
        source = "5.0.0"
        scanner = Scanner(source)
        c = scanner.advance()
        scanner.parse_number(c)
        self.assertTrue(scanner.had_error)

        self.scanner.source = "5\n5.0 6"
        c = self.scanner.advance()
        self.scanner.parse_number(c)
        self.scanner.advance()
        c = self.scanner.advance()
        scanner.parse_number(c)
        self.scanner.advance()
        c = self.scanner.advance()
        scanner.parse_number(c)
        print(self.scanner.tokens)

        self.assertEqual(self.scanner.tokens[0], Token(TokenType.NUMBER, "5", 5, 1))
        self.assertEqual(self.scanner.tokens[1], Token(TokenType.NUMBER, "5.0", 5.0, 2))
        self.assertEqual(self.scanner.tokens[2], Token(TokenType.NUMBER, "6", 6, 2))

    def test_parse_string(self):
        self.scanner.source = '"String Time"'
        self.scanner.advance()
        self.assertEqual(self.scanner.tokens[0], Token(TokenType.STRING, '"String Time"', "abc", 1))

        source = '"ABC'
        scanner= Scanner(source)
        scanner.advance()
        scanner.parse_string()
        self.assertTrue(scanner.had_error)

    def test_get_lexeme(self):
        self.scanner.start = 0
        self.scanner.current = 5
        self.assertEqual(self.scanner.get_lexeme(), "Hello")

if __name__ == '__main__':
    unittest.main()
