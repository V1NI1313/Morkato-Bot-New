from typing import (Optional, TypeVar, Callable, Generic, Union, Any)
from typing_extensions import (Self)
from .func import Route, getAll
from .hability import Hability
from functools import cache
from .family import Family
from discord.utils import get
import discord
### -> Exceptions <- ###
from .errors import (
  utilsError,
  GuildNotExists,
  UserAlreadyExists,
  ArgumentTypeNotSupported
)

Errors = {
  "GuildNotExists": GuildNotExists,
  "UserAlreadyExists": UserAlreadyExists
}
def setDictOptional(obj: dict, key: str, value: Any) -> dict:
  if value is None:
    return obj
  if isinstance(value, list):
    value = [(
      i
      if not isinstance(i, discord.Role)
      else i.id
      ) for i in value
    ]
  obj[key] = (
    value
    if not isinstance(value, discord.Role)
    else value.id
  )
  return obj
T = TypeVar('T')
class UserInventoryRolls(list, Generic[T]):
  def __init__(
    self,
    User,
    save: str,
    data: dict[str, Any],
    method: Callable[[Any], T],
    cls: object
  ) -> None:
    self.ep = User
    self.save = save
    _data = [[method(int(i))]*data[i] for i in data["inventory"]]
    data["inventory"] = []
    for i in _data:
      data["inventory"] = data["inventory"]+i
    super().__init__(data)
    self.__cls__ = cls
  def get(self, arg: Any) -> T:
    return self[self.index(arg)]
  def add(self, obj: T) -> None:
    if not isinstance(obj, self.__cls__):
      raise ArgumentTypeNotSupported(type(obj))
    self.append(obj)
    self.ep.edit(**{self.save: self.convertToDict()})
  def convertToDict(self) -> dict:
    json = {}
    for i in self:
      if i.id in json:
        continue
      json[str(i.id)] = len(getAll(self, i))
      return json
class User:
  def __init__(
    self,
    Guild,
    data: dict
  ) -> None:
    self.ep = Guild
    self.id: int = int(data["id"])
    self.breed: Optional[int] = data["breed"]
  def __repr__(self) -> str:
    return f"utilz.{type(self).__name__}(auth={self.auth} id={self.id})"
  def __eq__(self, __obj: Union[discord.Member, Self]) -> bool:
    if isinstance(__obj, discord.Member) or isinstance(__obj, User):
      return __obj.id == self.id
    return False
  @property
  def auth(self) -> discord.Member:
    return get(self.ep._ep.members, id=self.id)
  @property
  @cache
  def familys(self) -> UserInventoryRolls[Family]:
    return UserInventoryRolls(self, "family_rolls", self.get_data()["rolls"]["family"], getattr(self.ep.familys, "get"), Family)
  @property
  @cache
  def habilitys(self) -> UserInventoryRolls[Hability]:
    return UserInventoryRolls(self, "hability_rolls", self.get_data()["rolls"]["hability"], getattr(self.ep.habilitys, "get"), Hability)
  def get_data(self) -> dict:
    response = Route.get(f"/desktop/Guilds/{self.ep.id}/Users/{self.id}")
    if not response.status_code == 200:
      raise Errors.get(response.json()["message"], utilsError)(self.ep, self.auth)
    return response.json()
  def edit(self, **kwgs) -> Self:
    conflip = setDictOptional({"id": self.id}, "breed", kwgs.get("breed"))
    rolls = setDictOptional({}, "family", kwgs.get("family_rolls"))
    rolls = setDictOptional(rolls, "hability", kwgs.get("hability_rolls"))
    _data = {}
    if not len(conflip) == 1:
      _data = {**_data, **conflip}
    if not len(rolls):
      _data["rolls"] = rolls
    if not len(_data):
      return self
    response = Route.patch(
      f"/desktop/Guilds/{self.ep.id}/Users/{self.id}",
      data={
        **conflip,
        "rolls": rolls
      }
    )
    if not response.status_code == 200:
      raise utilsError(...)
    return self
def New_User(
  Guild,
  _User: discord.User
) -> User:
  response = Route.post(f"/desktop/Guilds/{Guild.id}/Users/{_User.id}", data={})
  if not response.status_code == 200:
    raise Errors.get(response.json()["message"], utilsError)(Guild, _User)
  return User(
    Guild,
    response.json()
  )