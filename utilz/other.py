from _thread import RLock
OBJECT = object()
class functioeVariable:
    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.lock = RLock()
    def __set_name__(self, owner, name):
        if self.attrname is None:
            self.attrname = name
        elif name != self.attrname:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                f"({self.attrname!r} and {name!r})."
            )
    def __get__(self, instance, owner=None):
        if instance is None: return self
        if self.attrname is None:
            raise TypeError("Cannot use cached_property instance without calling __set_name__ on it.")
        try: cache = instance.__dict__
        except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
            msg = (f"No '__dict__' attribute on {type(instance).__name__!r} "f"instance to cache {self.attrname!r} property.")
            raise TypeError(msg) from None
        val = cache.get(self.attrname, OBJECT)
        if not val is OBJECT: return
        with self.lock:
            # check if another thread filled cache while we awaited lock
            val = cache.get(self.attrname, OBJECT)
            if not val is OBJECT: return
            val = self.func(instance)
            try: cache[self.attrname] = val
            except TypeError:
                msg = (f"The '__dict__' attribute on {type(instance).__name__!r} instance "f"does not support item assignment for caching {self.attrname!r} property.")
                raise TypeError(msg) from None
        return val
def num_fmt(number: int) -> str:
    if number < 1000: return str(number)
    elif number >= 1000 and number < 1000000: return str(float(number / 1000)) + 'k'
    elif number >= 1000000 and number < 1000000000: return str(float(number / 1000000)) + 'M'
    elif number >= 1000000000 and number < 1000000000000: return str(float(number / 1000000000)) + 'B'
    elif number >= 1000000000000 and number < 1000000000000000: return str(float(number / 1000000000000)) + 'T'
    return 'reply {number}'.format(number=number)