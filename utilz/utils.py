from __future__ import annotations

from typing import (
  Optional,
  Callable,
  Generic,
  TypeVar,
  Tuple,
  Union,
  Iterable,
  Coroutine,
  overload,
  Self,
  Dict,
  List,
  Any,
  TYPE_CHECKING
)

import re

T = TypeVar('T')
T_co = Coroutine[Any, Any, T]

class _cached_variable:
  def __init__(self, function) -> None:
    self.function = function
    self.__doc__ = getattr(function, "__doc__")
  def __get__(self, isinstance, owner):
    if isinstance is None:
      return self
    value = self.function(isinstance)
    setattr(isinstance, self.function.__name__, value)
    return value
if TYPE_CHECKING:
  from functools import cached_property
else:
  cached_property = _cached_variable
class _Missing:
    __slots__ = ()
    def __is__(self, other) -> bool:
      return isinstance(other, _Missing)
    def __eq__(self, other) -> bool:
        return False
    def __bool__(self) -> bool:
        return False
    def __hash__(self) -> int:
        return 0
    def __repr__(self):
        return '...'

MISSING: Any = _Missing()

### -> attrgetter <- ###
class attrgetter:
  def __init__(self, attr, *attrs) -> None:
    if not attrs:
      if not isinstance(attr, str):
        raise TypeError('attribute name must be a string')
      self._attrs = (attr,)
      names = attr.split('.')
      def func(obj) -> Any:
        for name in names:
          obj = getattr(obj, name)
        return obj
      self._call = func
    else:
      self._attrs = (attr,) + attrs
      getters = tuple(map(attrgetter, self._attrs))
      def func(obj) -> Any:
        return tuple(getter(obj) for getter in getters)
      self._call = func
  def __call__(self, obj):
    return self._call(obj)

def get(iterable: Iterable[T], /, **attrs) -> T:
  """A helper that returns the first element in the iterable that meets
    all the traits passed in ``attrs``.
    
    To have a nested attribute search (i.e. search by ``x.y``) then
    pass in ``x__y`` as the keyword argument.

    If nothing is found that matches the attributes passed, then
    ``None`` is returned.
    
    Exemples:
    --------
    
    >>> utilz.utils.get(Guild.users, auth__name="Foo")
    >>> utilz.utils.get(Guild.habilitys, name="Foo")
  """
  attrget = attrgetter
  if len(attrs) == 1:
    key, value = attrs.popitem()
    pred = attrget(key.replace("__", '.'))
    return next((elem for elem in iterable if pred(elem) == value), None)
  converted = [(attrget(attr.replace('__', '.')), value) for attr, value in attrs.items()]
  for elem in iterable:
    if [None for pred, value in converted if pred(elem) == value]:
      return elem
  return None
class itemgetter:
    __slots__ = ('_attrs', '_call')
    def __init__(self, attr: str, *attrs) -> None:
      if not attrs:
        if not isinstance(attr, str):
          raise TypeError('attribute name must be a string')
        self._attrs = (attr,)
        names = attr.split('.')
        def func(obj: dict[str, Any]):
          for name in names:
            try: obj = obj.get(name)
            except NameError: break
          return obj
        self._call = func
    def __call__(self, obj: dict[str, Any]):
      return self._call(obj)
def getitem(dictionary: Iterable[dict[str, Any]], /, **kwgs):
  """Itemgetter of iterable dictionary.
  
  How to use? i'm get ``[{"name": "Foo"}, {"name": "afoo"}]``pass ``name="foo"``.
  
  i'm get ``name`` returned ``{"name": "Foo"}``
  
  How use use dictionary a dictionary? i'm get ``[{"info": {"name": "Foo"}}, {"info": {"name": "afoo"}}]`` pass ``info__name="afoo"``.
  
  i'm get ``info.foo`` returned ``{"info": {"name": "afoo"}}``
  
  Exemples:
  --------
  
  >>> utilz.utils.getitem([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}], id=3)
  >>> utilz.utils.getitem([{"info": {"id": 1}}, {"info": {"id": 2}}, {"info": {"id": 3}}], info__id=2)

  
  """
  itemget = itemgetter
  if len(kwgs) == 1:
    key, value = kwgs.popitem()
    pred = itemget(key.replace("__", '.'))
    return next((elem for elem in dictionary if pred(elem) == value), None)
class Typed_Dict:
  """Get a request from a typed dictionary

    Exemples:
    --------

    >>> typed_dict = utilz.utils.Typed_Dict({"name": str, "id": int, "role": (str, int)})
    >>> print(typed_dict({"name": "Foo", "id": 5505, "role": "foo"})) # output: True
    >>> print(typed_dict({"name": 93939, "id": 5505, "role": "foo"})) # output: False
  """
  __slots__ = ('obj',)
  def __init__(self, obj: dict[str, object]) -> None:
    self.obj = obj
  def __call__(self, other: dict[str, Any]) -> bool:
    if not len(self.obj) == len(other):
      return False
    for elem, other_elem in zip(self.obj.items(), other.items()):
      elem_key, elem_value = elem
      other_elem_key, other_elem_value = other_elem
      if not elem_key == other_elem_key:
        return False
      elem_value = (elem_value if not elem_value is None else type(None))
      if isinstance(elem_value, dict):
        elem_value = Typed_Dict(elem_value)
        if not elem_value(other_elem_value):
          return False
      elif not isinstance(other_elem_value, elem_value):
        return False
    return True
def check_typed_dict(dictionary_typed: dict[str, object], object: dict[str, Any]) -> bool:
  return Typed_Dict(dictionary_typed)(object)

class _utils:
  @cached_property
  def format(self):
    return re.compile("\${(?P<key>[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ_]+)}")
utils = _utils()
class text(str):
  def format(self, **kwargs) -> text:
    text: str = str(self)
    while True:
      response = utils.format.search(text)
      if response is None:
        return text
      key = response.group("key")
      left, right = response.span()
      text = text[:left] + kwargs.get(key, '{NOTITEM}') + text[right:]

class Switch(Generic[T]):
  __slots__ = ('case',)
  def __init__(self, obj: T) -> None:
    def __call__(attr: T, /, func: Optional[Callable[[], None]]=lambda: 0) -> bool:
      value = obj == attr
      if hasattr(func, '__call__'):
        func()
      return value
    self.case = __call__
  def __call__(self, attr: T, /, func: Optional[Callable[[], None]]=None) -> bool:
    return self.case(attr, func)