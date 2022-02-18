from .compare_funcs import comparatives

def isEqual(dimensional_data, data, value):
    comparatives['equal'](dimensional_data.get(data), value)

def isDifferent(dimensional_data, data, value):
    comparatives['different'](dimensional_data.get(data), value)

def isLower(dimensional_data, data, value):
    comparatives['lower'](dimensional_data.get(data), value)

def isGreater(dimensional_data, data, value):
    comparatives['greater'](dimensional_data.get(data), value)

def isBetween(dimensional_data, data, _min, _max):
    comparatives['between'](dimensional_data.get(data), _min, _max)

data_comparatives = {
    'equal': isEqual,
    'different': isDifferent,
    'lower': isLower,
    'greater': isGreater,
    'between': isBetween
}