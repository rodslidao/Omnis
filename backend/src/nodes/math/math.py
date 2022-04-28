import math
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
