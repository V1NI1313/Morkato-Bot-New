import ast
import json
from typing import (
    Any,
    Dict,
    Union,
    overload
)
class objectContext:
    def __init__(self, object: Union[Any, Any, Dict]):
        self.__dict__ = object
        for i in self.__dict__:
            if type(self.__dict__[i]) is dict: self.__dict__[i] = objectContext(self.__dict__[i])
    def __repr__(self) -> str: return str(self.__dict__)
    def __str__(self) -> str: return self.__repr__()
    def __len__(self) -> int: return self.__dict__.__len__()
    def __todictall__(self) -> None:
        chr = self.__dict__
        for i in chr:
            if type(chr[i]) is objectContext: chr[i] = chr[i].__todictall__()
        return chr
    def __getitem__(self, __key: Union[str, int, Any, Any]):
        if type(__key) is str: return self.__dict__[__key]
        elif type(__key) is int: return self.__dict__[list(self.__dict__.keys())[__key]]
    def __setitem__(self, __key: Union[str, int, Any, Any], __value: Any):
        if type(__key) is str: self.__dict__[__key] = __value
        elif type(__key) is int: self.__dict__[list(self.__dict__.keys())[__key]] = __value
    def __saveall__(self, file: str, indent: int=None) -> Union[Any, Dict[str, Any]]:
        with open(file, 'w') as a: json.dump(self.__todictall__(), a, indent=indent)
    def __setup__(self): print('pegou!')
def openObjectJS(file: str):
    with open(file, 'r') as a:
        __dict = objectContext(ast.literal_eval(a.read()))
    return __dict
def saveall(__object: Union[Any, Any, objectContext], file: str, *, indent: int=None) -> Union[Any, Dict[str, Any]]:
    return __object.__saveall__(file, indent)
if __name__ == '__main__': OBJECT = openObjectJS('forms.json')
