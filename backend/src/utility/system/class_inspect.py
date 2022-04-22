from inspect import getmro, isroutine

def is_static_method(klass, attr, value=None):
    """Test if a value of a class is static method.
    example::
        class MyClass(object):
            @staticmethod
            def method():
                ...
    :param klass: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    for cls in getmro(klass):
        if isroutine(value):
            if attr in cls.__dict__:
                binded_value = cls.__dict__[attr]
                return isinstance(binded_value, staticmethod)
    return False