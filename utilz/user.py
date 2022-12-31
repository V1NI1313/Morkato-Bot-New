from __future__ import annotations

from typing import TYPE_CHECKING
from .func import Route, getAll
from .hability import Hability
from .family import Family
from . import utils
import discord
### -> Exceptions <- ###
from .errors import (
  utilsError,
  GuildNotExists,
  UserAlreadyExists,
  ArgumentTypeNotSupported,
  ResponseError,
  NotChoices
)

if TYPE_CHECKING:
  from .guild import Guild

Errors = {
  "GuildNotExists": GuildNotExists,
  "UserAlreadyExists": UserAlreadyExists
}
def setDictOptional(obj: dict, key: str, value: utils.Any) -> dict:
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
T = utils.TypeVar('T')
class UserInventoryRolls(list, utils.Generic[T]):
  def __init__(
    self,
    User: User,
    save: tuple[str],
    data: dict[str, utils.Any],
    method: utils.Callable[[int], T],
    cls: T
  ) -> None:
    self.dict: dict[int, int] = dict(map(lambda elem: (int(elem[0]), (method(int(elem[0])), elem[1]),), data["inventory"].items()))
    self.choice: int = data["choice"]
    self.__cls__: cls = cls
    self.save = save
    self.ep = User
    
    super().__init__(self.dict.values())
  def __repr__(self) -> str:
    return "[ \n  %s\n ]"%((", \n".join(map(lambda elem: f"  {elem}", self))).strip(", \n"))
  def get(self, /, id: int) -> utils.Optional[T]:
    return self.dict.get(id)
  def add(self, /, obj: T) -> None:
    if not isinstance(obj, self.__cls__):
      raise ArgumentTypeNotSupported(type(obj))
    if self.choice == 0:
      raise NotChoices(f"Not choices of user id {self.ep.id}")
    self.choice -= 1
    if obj.id in self.dict:
      index = self.index(self.get(obj.id))
      self.dict[obj.id] = (obj, self.dict[obj.id][1]+1)
      self[index] = self.dict[obj.id]
    else:
      self.dict[obj.id] = (obj, 1)
      self += [(self.dict[obj.id]),]
    self.ep.edit(**{self.save[0]: self.toJson(), self.save[1]: self.choice})
  def toJson(self) -> dict:
    return dict(map(lambda elem: (str(elem[0].id), elem[1]), self.dict.values()))
class UserFamilyRolls(UserInventoryRolls):
  def __init__(
    self,
    user
  ) -> None: super().__init__(
    User=user,
    save=("family_rolls", "family_choice"),
    data=user.get_data()["rolls"]["family"],
    method=getattr(user.ep.familys, "get"),
    cls=Family
  )
class UserHabilityRolls(UserInventoryRolls):
  def __init__(
    self,
    user
  ) -> None: super().__init__(
    User=user,
    save=("hability_rolls", "hability_choice"),
    data=user.get_data()["rolls"]["hability"],
    method=getattr(user.ep.habilitys, "get"),
    cls=Hability
  )
class User:
  def __init__(
    self,
    Guild,
    /, data: dict
  ) -> None:
    self.ep = Guild
    self.id: int = int(data["id"])
    self.breed: utils.Optional[int] = data["breed"]
  def __eq__(self, user: User) -> bool:
    if not isinstance(user, User):
      return False
    return self.id == user.id
  @property
  def auth(self) -> discord.Member:
    return utils.get(self.ep._ep.members, id=self.id)
  @utils.cached_property
  def rolls_familys(self) -> UserInventoryRolls[Family]:
    return UserFamilyRolls(self)
  @utils.cached_property
  def rolls_habilitys(self) -> UserInventoryRolls[Hability]:
    return UserHabilityRolls(self)
  def get_data(self) -> dict:
    response = Route.get(f"/desktop/Guilds/{self.ep.id}/Users/{self.id}")
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection the guild id {self.ep.id} of user id {self.id}")
    return response.json()
  def edit(self, **kwgs) -> utils.Self:
    conflip = setDictOptional({}, "breed", kwgs.get("breed"))
    family_rolls = setDictOptional({}, "choice", kwgs.get("family_choice"))
    family_rolls = setDictOptional(family_rolls, "inventory", kwgs.get("family_rolls"))
    hability_rolls = setDictOptional({}, "choice", kwgs.get("hability_choice"))
    hability_rolls = setDictOptional(hability_rolls, "inventory", kwgs.get("hability_rolls"))
    if len(family_rolls):
      try: conflip["rolls"]["family"] = family_rolls
      except: conflip["rolls"] = {"family": family_rolls}
    if len(hability_rolls):
      try: conflip["rolls"]["hability"] = hability_rolls
      except: conflip["rolls"] = {"hability": hability_rolls}
    if not len(conflip):
      return self
    response = Route.patch(
      f"/desktop/Guilds/{self.ep.id}/Users/{self.id}",
      data=conflip,
      headers={
        "content-type": "application/json"
      }
    )
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection user id {self.id} of guild id {self.ep.id}")
    self.__init__(self.ep, response.json())
    return self
def New_User(
  Guild: Guild,
  user: discord.User
) -> User:
  response = Route.post(f"/desktop/Guilds/{Guild.id}/Users/{user.id}", data={})
  if not response.status_code == 200:
    raise ResponseError(f"Failhed connection user id {user.id} of guild id {Guild.id}")
  return User(
    Guild,
    response.json()
  )