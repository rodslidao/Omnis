from inspect import getmro, isroutine


def is_static_method(clss, attr, value=None):
    """Test if a value of a class is static method.
    example::
        class MyClass(object):
            @staticmethod
            def method():
                ...
    :param clss: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if value is None:
        value = getattr(clss, attr)
    assert getattr(clss, attr) == value

    for cls in getmro(clss):
        if isroutine(value):
            if attr in cls.__dict__:
                blinded_value = cls.__dict__[attr]
                return isinstance(blinded_value, staticmethod)
    return False
