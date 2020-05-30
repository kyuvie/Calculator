from b1u3calculator import ast, token

import unittest


class AstTest(unittest.TestCase):
    def test_assign_stmt_str(self):
        program = ast.Program()
        program.statements = [
                ast.AssignStatement(
                    token=token.Token(token.ID, "myVar"),
                    name=ast.Identifier(token=token.Token(token.ID, "myVar"), value="myVar"),
                    value=ast.Identifier(token=token.Token(token.ID, "anotherVar"), value="anotherVar")
                )
        ]
        self.assertEqual(str(program), "myVar = anotherVar;", f'expect "myVar = anotherVar", got = {str(program)}')


