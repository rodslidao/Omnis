import math
from api import logger, exception, for_all_methods
_sum = lambda x, y: x + y
_sub = lambda x, y: x - y
_mul = lambda x, y: x * y
_div = lambda x, y: x / y
_mod = lambda x, y: x % y
_pow = lambda x, y: math.pow(x, y)
_sqrt = lambda x: math.sqrt(x)
_log = lambda x: math.log(x)
_log10 = lambda x: math.log10(x)
_sin = lambda x: math.sin(math.radians(x))
_cos = lambda x: math.cos(math.radians(x))
_tan = lambda x: math.tan(math.radians(x))
_atan = lambda x: math.atan(math.radians(x))
_asin = lambda x: math.asin(math.radians(x))
_acos = lambda x: math.acos(math.radians(x))
_trunc = lambda x: math.trunc(x)

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