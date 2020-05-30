import unittest 
from b1u3calculator import token, lexer


class LexerTest(unittest.TestCase):
    def test_next_token1(self):
        input = "=+-*/(){},;"
        tests = [
                [token.ASSIGN, "="],
                [token.PLUS, "+"],
                [token.MINUS, "-"],
                [token.ASTER, "*"],
                [token.SLASH, "/"],
                [token.LPAREN, "("],
                [token.RPAREN, ")"],
                [token.LBRACE, "{"],
                [token.RBRACE, "}"],
                [token.COMMA, ","],
                [token.SEMICOLON, ";"],
                [token.EOF, ""]
                ]
        l = lexer.Lexer(input)
        for i, tt in enumerate(tests):
            tok = l.next_token()
            self.assertEqual(tok.type, tt[0])
            self.assertEqual(tok.literal, tt[1])

    def test_next_token2(self):
        input = "five = 5; ten = 10; def add(a, b, c) { return a + b + c }; result = add(five, ten, ten);"
        tests = [
                [token.ID, "five"],
                [token.ASSIGN, "="],
                [token.INT, "5"],
                [token.SEMICOLON, ";"],
                [token.ID, "ten"],
                [token.ASSIGN, "="],
                [token.INT, "10"],
                [token.SEMICOLON, ";"],
                [token.FUNCTION, "def"],
                [token.ID, "add"],
                [token.LPAREN, "("],
                [token.ID, "a"],
                [token.COMMA, ","],
                [token.ID, "b"],
                [token.COMMA, ","],
                [token.ID, "c"],
                [token.RPAREN, ")"],
                [token.LBRACE, "{"],
                [token.RETURN, "return"],
                [token.ID, "a"],
                [token.PLUS, "+"],
                [token.ID, "b"],
                [token.PLUS, "+"],
                [token.ID, "c"],
                [token.RBRACE, "}"],
                [token.SEMICOLON, ";"],
                [token.ID, "result"],
                [token.ASSIGN, "="],
                [token.ID, "add"],
                [token.LPAREN, "("],
                [token.ID, "five"],
                [token.COMMA, ","],
                [token.ID, "ten"],
                [token.COMMA, ","],
                [token.ID, "ten"],
                [token.RPAREN, ")"],
                [token.SEMICOLON, ";"],
                [token.EOF, ""]
                ]

        l = lexer.Lexer(input)
        for i, tt in enumerate(tests):
            tok = l.next_token()
            self.assertEqual(tok.type, tt[0], f"{i} test is error")
            self.assertEqual(tok.literal, tt[1])

