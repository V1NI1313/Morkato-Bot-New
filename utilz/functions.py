def formatstr(__text__: str, **kwgs) -> str:
    kwargs = {}
    for i in kwgs:
        kwargs["${0}{arg}{1}".format("{", "}", arg=i)] = kwgs[i]
    for i in kwargs:
        __text__ = __text__.replace(i, kwargs[i])
    return __text__
def FormatRarety(number: int) -> str:
    if number == 0: return "commom"
    elif number == 1: return "rare"
    elif number == 2: return "epic"
    elif number == 3: return "legendary"
def endswith(text: str, _chr: list[str]) -> bool:
    for i in _chr:
        if text.endswith(i):
            return True
    return False
class Conflip:
    def __init__(self, **kwgs):
        self.message = kwgs.get("message")
        self.channel = kwgs.get("channel")
        self.guild = kwgs.get("guild")