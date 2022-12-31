from __future__ import annotations

from typing import TYPE_CHECKING
from functools import cache
from .family import Family
from .func import Route
from .user import User
from . import utils
import discord
### -> Exceptions <- ###
from .errors import utilsError, ResponseError

if TYPE_CHECKING:
  from .guild import Guild

class UserNotFamily(utilsError):
  def __init__(self, user: User, family: Family) -> None:
    super().__init__(f"Family id {family.id} not in inventory User id {user.id}")
class PlayerAlreadyExists(utilsError):
  def __init__(self, player: Player) -> None:
    super().__init__(f"Player id {player.id} already exists!")
class Player(User):
  def __init__(
    self,
    Guild,
    data: dict[str, dict]
  ) -> None: super().__init__(Guild, data)
  def __repr__(self) -> str:
    return "utilz.Player(...)"
  def __eq__(self) -> bool: ...
  @property
  @cache
  def settings(self): ...
  def get_data(self) -> dict:
    response = Route.get(f"/desktop/Guilds/{self.ep.id}/Users/{self.id}")
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection the guild id {self.ep.id} of user id {self.id}")
    user = response.json()
    return {**user["User"], **user["Player"]}
  def edit(self, **kwgs) -> None: ...
def New_Player(
  Guild: Guild,
  user: User, /,
  *, name: str,
  surname: utils.Optional[str]=None,
  age: int,
  family: Family
) -> Player:
  if user.rolls_familys.get(family.id) is None:
    raise UserNotFamily(user, family)
  data = {
    "name": name,
    "nick": surname,
    "age": age,
    "family": str(family.id)
  }; response = Route.post(
    f"/desktop/Guilds/{Guild.id}/Players/{user.id}",
    data=data,
    headers={
      "content-type": "application/json"
    }
  ); switch = utils.Switch(response.status_code)
  if switch(200):
    return Player(Guild, response.json())
  elif switch(403):
    raise PlayerAlreadyExists(Guild.players.get(user.id))
  elif switch(404):
    raise ResponseError(f"Failhed connection the guild id {Guild.id} of user id {user.id}")
  
  