import unittest
from scanner.scanner import Scanner


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

if __name__ == '__main__':
    unittest.main()
