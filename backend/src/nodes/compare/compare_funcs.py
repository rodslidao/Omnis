# For all possible logical comparative between two values, make a function:

def isEqual(value1, value2, *args):
    return value1 == value2

def isDifferent(value1, value2, *args):
    return value1 != value2

def isGreater(value1, value2, *args):
    return value1 >= value2

def isLower(value1, value2, *args):
    return value1 <= value2

def isBetween(value1, value2, value3, *args):
    return value1 >= value2 and value1 <= value3

comparatives = {
    'equal': isEqual,
    'different': isDifferent,
    'lower': isLower,
    'greater': isGreater,
    'between': isBetween
}