import unittest
from b1u3calculator import ast, lexer, parser


class ParserTest(unittest.TestCase):
    def test_assign_statement(self):
        input = "a = 5; b = 5; c = 10;"
        l = lexer.Lexer(input)
        p = parser.Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)
        self.assertEqual(type(program), ast.Program)
        self.assertEqual(len(program.statements), 3)
        tests = [
                "a",
                "b",
                "c",
                ]
        for i, tt in enumerate(tests):
            stmt = program.statements[i]
            self.help_test_assign_statement(stmt, tt[0], i)


    def help_test_assign_statement(self, stmt, e_name, index):
        self.assertEqual(type(stmt), ast.AssignStatement, f"{index} test is {type(stmt)} != {ast.AssignStatement}")
        self.assertEqual(stmt.name.value, e_name, f"{index} test is {stmt.name.value} != {e_name}")
        self.assertEqual(stmt.name.token_literal(), e_name, f"{index} test is {stmt.name.token_literal()} != {e_name}")

    def check_parser_errors(self, p):
        if len(p.errors) != 0:
            self.fail("\n".join(p.errors))

    def test_return_statement(self):
        input = "return 5; return a; return a * b;"
        l = lexer.Lexer(input)
        p = parser.Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)
        self.assertEqual(type(program), ast.Program)
        self.assertEqual(len(program.statements), 3)
        for stmt in program.statements:
            self.assertEqual(type(stmt), ast.ReturnStatement)
            self.assertEqual(stmt.token_literal(), "return")

    def test_identifier_expression(self):
        input = "foobar;"
        l = lexer.Lexer(input)
        p = parser.Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)
        self.assertEqual(len(program.statements), 1)
        self.assertEqual(type(program.statements[0]), ast.ExpressionStatement)
        self.assertEqual(type(program.statements[0].expression), ast.Identifier)
        ident = program.statements[0].expression
        self.assertEqual(ident.value, "foobar")
        self.assertEqual(ident.token_literal(), "foobar")


    def test_integer_literal_expression(self):
        input = "5;"
        l = lexer.Lexer(input)
        p = parser.Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)
        self.assertEqual(len(program.statements), 1)
        self.assertEqual(type(program.statements[0]), ast.ExpressionStatement)
        self.assertEqual(type(program.statements[0].expression), ast.IntegerLiteral)
        ident = program.statements[0].expression
        self.assertEqual(ident.value, 5)
        self.assertEqual(ident.token_literal(), "5")


    def test_prefix_expression(self):
        input = "-5;"
        l = lexer.Lexer(input)
        p = parser.Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)
        self.assertEqual(len(program.statements), 1)
        self.assertEqual(type(program.statements[0]), ast.ExpressionStatement)
        self.assertEqual(type(program.statements[0].expression), ast.PrefixExpression)
        prefix = program.statements[0].expression
        self.help_test_integer_literal(prefix.right, 5)
        self.assertEqual(prefix.operator, "-")

    def help_test_integer_literal(self, exp, value):
        self.assertEqual(type(exp), ast.IntegerLiteral)
        self.assertEqual(exp.value, value)

    def test_infix_expression(self):
        tests = [
                ["7 + 5;", 7, "+", 5],
                ["7 - 5;", 7, "-", 5],
                ["7 * 5;", 7, "*", 5],
                ["7 / 5;", 7, "/", 5]
                ]
        for tt in tests:
            l = lexer.Lexer(tt[0])
            p = parser.Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)
            self.assertEqual(len(program.statements), 1)
            self.assertEqual(type(program.statements[0]), ast.ExpressionStatement)
            self.assertEqual(type(program.statements[0].expression), ast.InfixExpression)
            infix = program.statements[0].expression
            self.assertEqual(infix.operator, tt[2])
            self.help_test_integer_literal(infix.right, tt[3])
            self.help_test_integer_literal(infix.left, tt[1])

    def test_operator_precedence(self):
        tests = [
                ["-a * b", "((-a) * b)"],
                ["a + b + c", "((a + b) + c)"],
                ["-a - b - c", "(((-a) - b) - c)"],
                ["a / b / c", "((a / b) / c)"],
                [" a + b * c / d - e", "((a + ((b * c) / d)) - e)"]
                ]
        for tt in tests:
            l = lexer.Lexer(tt[0])
            p = parser.Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)
            self.assertEqual(len(program.statements), 1)
            self.assertEqual(type(program.statements[0]), ast.ExpressionStatement)
            self.assertEqual(str(program.statements[0]), tt[1])

    def test_grouped_precedence(self):
        tests = [
                ["-a * b", "((-a) * b)"],
                ["a + (b + c)", "(a + (b + c))"],
                ["(a + b) + c", "((a + b) + c)"],
                ["-a - (b - c)", "((-a) - (b - c))"],
                ["((-a - b) - c)", "(((-a) - b) - c)"],
                ["a / (b / c)", "(a / (b / c))"],
                ["(-a / b) / c", "(((-a) / b) / c)"],
                ["a + b * c / (d - e)", "(a + ((b * c) / (d - e)))"]
                ]
        for tt in tests:
            l = lexer.Lexer(tt[0])
            p = parser.Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)
            self.assertEqual(len(program.statements), 1)
            self.assertEqual(type(program.statements[0]), ast.ExpressionStatement)
            self.assertEqual(str(program.statements[0]), tt[1])

    def test_function_define(self):
        tests = [
                ["def a(abc, abc, def) {a + b + c;}", 3],
                ["def abcde() { return a + b; }", 0]
                ]
        for i, tt in enumerate(tests):
            l = lexer.Lexer(tt[0])
            p = parser.Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)
            self.assertEqual(len(program.statements), 1)
            stmt = program.statements[0]
            self.assertEqual(type(stmt), ast.FunctionStatement)
            self.assertEqual(type(stmt.id), ast.Identifier)
            self.assertEqual(type(stmt.block), ast.BlockStatement)
            self.help_test_function(stmt, tt[1])

    def help_test_function(self, exp, spara):
            self.assertEqual(len(exp.parameters), spara)


    def test_call_expression(self):
        tests = [
                ["add(1, 2, 3);", 3],
                ["add(1+2, 2/3);", 2]
                ]
        for tt in tests:
            l = lexer.Lexer(tt[0])
            p = parser.Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)
            self.assertEqual(len(program.statements), 1)
            self.assertEqual(type(program.statements[0]), ast.ExpressionStatement)
            stmt = program.statements[0]
            exp = stmt.expression
            self.assertEqual(type(exp), ast.CallExpression)
            self.assertEqual(type(exp.function), ast.Identifier)
            self.assertEqual(len(exp.arguments), tt[1])
            if tt[1] != 0:
                self.assertTrue(isinstance(exp.arguments[0], ast.ExpressionNode))


    def test_assign_completion(self):
        tests = [
                ["abc = 3 * 4;", ast.InfixExpression],
                ["abcde = add(3);", ast.CallExpression]
                ]
        for tt in tests:
            l = lexer.Lexer(tt[0])
            p = parser.Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)
            self.assertEqual(len(program.statements), 1)
            self.assertEqual(type(program.statements[0]), ast.AssignStatement)
            stmt = program.statements[0]
            exp = stmt.value
            self.assertEqual(type(exp), tt[1])


    def test_return_completion(self):
        tests = [
                ["return a * b * 3;", ast.InfixExpression],
                ["return add(3);", ast.CallExpression]
                ]
        for tt in tests:
            l = lexer.Lexer(tt[0])
            p = parser.Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)
            self.assertEqual(len(program.statements), 1)
            self.assertEqual(type(program.statements[0]), ast.ReturnStatement)
            stmt = program.statements[0]
            exp = stmt.return_value
            self.assertEqual(type(exp), tt[1])

