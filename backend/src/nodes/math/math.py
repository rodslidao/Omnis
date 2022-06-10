from __future__ import division
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
import math
import operator
from api import logger, exception


def _sum(x, y):
    return x + y

def _sub(x, y):
    return x - y

def _mul(x, y):
    return x * y

def _div(x, y):
    return x / y


def _mod(x, y):
    return x % y

def _pow(x, y):
    return math.pow(x, y)


def _sqrt(x):
    return math.sqrt(x)

def _log(x):
    return math.log(x)

def _log10(x):
    return math.log10(x)

def _sin(x):
    return math.sin(math.radians(x))


def _cos(x):
    return math.cos(math.radians(x))

def _tan(x):
    return math.tan(math.radians(x))

def _atan(x):
    return math.atan(math.radians(x))

def _asin(x):
    return math.asin(math.radians(x))

def _acos(x):
    return math.acos(math.radians(x))

def _trunc(x):
    return math.trunc(x)

calcs = {
    "+": _sum,
    "-": _sub,
    "*": _mul,
    "/": _div,
    "%": _mod,
    "^": _pow,
    "sqrt": _sqrt,
    "log": _log,
    "log10": _log10,
    "sin": _sin,
    "cos": _cos,
    "tan": _tan,
    "atan": _atan,
    "asin": _asin,
    "acos": _acos,
    "round": round,
    "int": _trunc,
}


@exception(logger)
def calculate(x, op, y=None):
    match x, y:
        case None, None:
            return None
        case None, _:
            return calcs[op](y)
        case _, None:
            return calcs[op](x)
        case _, _:
            return calcs[op](x, y)


@exception(logger)
def resolve_exression(expression):
    for k in range(0, len(expression), 2):
        if isinstance(expression[k], list):
            expression[k] = resolve_exression(expression[k])
        else:
            return calculate(*expression)
    if type(expression) is list:
        return calculate(*expression)

class NumericStringParser(object):
    __author__ = 'Paul McGuire'
    __source__ = '''http://pyparsing.wikispaces.com/file/view/fourFn.py
    http://pyparsing.wikispaces.com/message/view/home/15549426
    '''
    __note__ = '''
    All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
    more easily in other places.
    '''

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + \
            ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "exp": math.exp,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "pi":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val
