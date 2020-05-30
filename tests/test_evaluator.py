import unittest
from b1u3calculator import lexer, parser, obj, evaluator
import logging



class EvaluatorTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(filename="evaluator_test.log", filemode='w', level=logging.DEBUG)

    def test_integer_object(self):
        tests = [
                ["5;", 5],
                ["9", 9]
                ]
        for i, tt in enumerate(tests):
            obj = self.help_eval(tt[0])
            self.help_equal_int(obj, tt[1], i)

    def help_eval(self, s):
        l = lexer.Lexer(s)
        p = parser.Parser(l)
        program = p.parse_program()
        env = {}
        funcs = {}
        try:
            return evaluator.eval(program, env, funcs)
        except evaluator.EvaluatedError:
            print(env)
            pass


    def help_equal_int(self, o, v, ind):
        print(type(o))
        self.assertTrue(isinstance(o, obj.Integer), f"tests[{ind}]  {type(obj)} is not obj.Integer")
        self.assertEqual(o.value, v, f"{o.value} is not {v}")

    def test_prefix(self):
        """ Testing conversion of Prefix Expression to Integer Object"""
        tests = [
                ["-5;", -5],
                ["--9", 9],
                ["9; -8", -8]
                ]
        for i, tt in enumerate(tests):
            obj = self.help_eval(tt[0])
            self.help_equal_int(obj, tt[1], i)

    def test_infix(self):
        """ Testing conversion of Prefix Expression to Integer Object"""
        tests = [
                ["5+7;", 12],
                ["8+-7-1", 0],
                ["1 + 3 * 4 / 3 + 2", 7]
                ]
        for i, tt in enumerate(tests):
            obj = self.help_eval(tt[0])
            self.help_equal_int(obj, tt[1], i)

    def test_return(self):
        tests = [
                ["return 12;", 12],
                ["return 0 + 0 * 300", 0],
                ["return 3; return 4", 3]
                ]
        for i, tt in enumerate(tests):
            obj = self.help_eval(tt[0])
            self.help_equal_int(obj, tt[1], i)

    def test_let_stmt(self):
        tests = [
                ["a = 5; a;", 5],
                ["a = 5 * 5; a;", 25],
                ["a = 5; b = a; b;", 5],
                ["a = 5; b = a; c = a + b + 5; c;", 15]
                ]
        for i, tt in enumerate(tests):
            obj = self.help_eval(tt[0])
            self.help_equal_int(obj, tt[1], i)

    def test_def_func(self):
        tests = [
                ["def abc(a, b, c) { return a + b + c}; abc(1, 2, 3)", 6],
                ["def abc(a, b, c) { d = 4; return a + b + c + d; a = 100}; abc(1, 2, 3);", 10],
                ["def abc(a, b, c) {}; abc(0, 0, 0)", 0]
                ]
        for i, tt in enumerate(tests):
            obj = self.help_eval(tt[0])
            self.help_equal_int(obj, tt[1], i)

    def test_error1(self):
        tests = [
                ["def abc(a, b, c) { return a + b + c }; abc(1*2, 2*3, 3 * 4)", 20]
                ]
        for i, tt in enumerate(tests):
            obj = self.help_eval(tt[0])
            self.help_equal_int(obj, tt[1], i)

