from __future__ import annotations

from typing import TYPE_CHECKING
from .func import Route
from . import utils
### -> Exceptions <- ###
from .errors import ResponseError

if TYPE_CHECKING:
  from .guild import Guild
T = utils.TypeVar('T')

class _GuildMethods(utils.Generic[T]):
  def get(self, elem: GuildElements, /, id: int) -> utils.Optional[T]: ...
  def new(self, elem: GuildElements, /, **attrs) -> utils.Optional[T]: ...

# Global to Local
GuildMethods = _GuildMethods()
MISSING = utils.MISSING

class GuildElements(list, utils.Generic[T]):
  getter: utils.Callable[[int], T]
  setter: utils.Callable[[Guild, MISSING], T]
  def __init__(
    self,
    Guild: Guild,
    iterable: utils.Iterable[dict[str, utils.Any]],
    cls: T,
    /,  *, getMethod: utils.Callable[[int], T]=GuildMethods.get,
    newMethod: utils.Callable[[Guild, MISSING], T]=GuildMethods.new
  ) -> None:
    self.dict: dict[int, T] = dict([(int(elem['id']), cls(Guild, elem)) for elem in iterable])
    super().__init__(self.dict.values())
    self.getter = getMethod
    self.setter = newMethod
    self.__cls__ = cls
    self.ep = Guild
  def get(self, /, id: int) -> utils.Optional[T]:
    return self.dict.get(id)
  def new(self, /, *args, **attrs: dict[str, utils.Any]) -> T:
    obj: self.__cls__ = self.setter(self.ep, *args, **attrs)
    self.dict[obj.id] = obj
    self.append(obj)
    return obj
class GuildElementsFilter(GuildElements, utils.Generic[T]):
  def _filter(self, iterable: utils.Optional[GuildElements[T]]=None):
    iterable = (iterable if not iterable is None else self)
    json = {0: [], 1: [], 2: [], 3: []}
    for i in iterable:
      json[i.rarity] += [i,]
    return json
class _GuildSettings:
  def __init__(self, Guild: Guild) -> None:
    self.ep = Guild
  def __getitem__(self, key: str) -> utils.Union[bool, int]:
    value = getattr(self, key)
    if value is None:
      raise KeyError(f"Key `{key}` not exists!")
    return value
  def edit(self, **kwgs) -> None:
    response = Route.patch(
      f"/desktop/Guilds/{self.ep._ep.id}",
      data=self.ep.data,
      headers={
        "content-type": "application/json"
      }
    )
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection of guild id {self.ep.id}")
    return response.json()
  @property
  def playerBreed(self) -> int:
    return self.ep.get_data()["settings"]["playerBreed"]