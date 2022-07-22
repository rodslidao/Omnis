from src.utility.system.class_inspect import is_static_method


def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if (
                callable(getattr(cls, attr))
                and not attr.startswith("__")
                and not is_static_method(cls, attr)
            ):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate
