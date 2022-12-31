from __future__ import annotations

from .guild_utils import GuildElements, GuildElementsFilter, _GuildSettings
from .hability import (Hability, New_Hability)
from .family import (Family, New_Family)
from .player import (Player, New_Player)
from .user import (User, New_User)
from random import randint
from .func import Route
from . import utils
import discord
### -> Exceptions <- ###
from .errors import (
  utilsError,
  GuildNotExists,
  GuildAlreadyExists,
  FamilyNotExists,
  HabilityNotExists,
  PlayerNotExists,
  UserNotExists,
  ResponseError
)
typed_player = utils.Typed_Dict({})
GuildErrors = {
  "GuildNotExists": GuildNotExists,
  "GuildAlreadyExists": GuildAlreadyExists
}
T = utils.TypeVar('T')
MISSING = utils.MISSING

class Guild:
  def __init__(
    self,
    Guild: discord.Guild,
    data: dict[str, utils.Any]
  ) -> None:
    self._ep = Guild
    self.data = data
    self.id = Guild.id
    
    self.human_roleID: utils.Optional[int] = int(data["roles"]["human"])
    self.oni_roleID: utils.Optional[int] = int(data["roles"]["oni"])
    self.hybrid_roleID: utils.Optional[int] = int(data["roles"]["hybrid"])
  @classmethod
  def from_guild(
    cls,
    _Guild: discord.Guild
  ) -> Guild:
    response = Route.get(f"/desktop/Guilds/{_Guild.id}")
    if not response.status_code == 200:
      raise GuildErrors.get(response.json()["message"], Exception)(_Guild)
    return cls(
      Guild=_Guild,
      data=response.json()
    )
  @property
  def human_role(self) -> utils.Optional[discord.Role]:
    return self._ep.get_role(self.human_roleID)
  @property
  def oni_role(self) -> utils.Optional[discord.Role]:
    return self._ep.get_role(self.oni_roleID)
  @property
  def hybrid_role(self) -> utils.Optional[discord.Role]:
    return self._ep.get_role(self.hybrid_roleID)
  @utils.cached_property
  def settings(self) -> _GuildSettings:
    return _GuildSettings(self)
  @utils.cached_property
  def habilitys(self) -> utils.Union[GuildElements[Hability], _GuildHabilitys]:
    return _GuildHabilitys(self)
  @utils.cached_property
  def familys(self) -> utils.Union[GuildElements[Family], _GuildFamilys]:
    return _GuildFamilys(self)
  @utils.cached_property
  def users(self) -> utils.Union[GuildElements[User], _GuildUsers]:
    return _GuildUsers(self)
  @utils.cached_property
  def players(self) -> GuildPlayers:
    return GuildPlayers(self)
  def get_data(self) -> dict[str, utils.Any]:
    response = Route.get(f"/desktop/Guilds/{self.id}")
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection guild id {self.id}")
    return response.json()
  def edit(self, **kwgs) -> None: ...
class _GuildHabilitys(GuildElementsFilter):
  def __init__(self, Guild: Guild) -> None:
    response = Route.get(f"/desktop/Guilds/{Guild.id}/Hability")
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection guild id {self.id} habilitys")
    super().__init__(Guild, response.json(), Hability, newMethod=New_Hability)
  def fromUser(self, User: User) -> utils.Optional[list[Hability]]:
    habilitys = [self.get(int(i)) for i in User.rolls_habilitys.toJson()]
    return (habilitys if len(habilitys) else None)
  def fromRequireUser(self, User: User) -> utils.Optional[list[Hability]]:
    habilitys = [i for i in self if i.verificationUser(User)]
    return (habilitys if len(habilitys) else None)
  def filter(self, User: utils.Optional[User]=None) -> utils.Optional[dict[int, list[Hability]]]:
    habilitys = ((self if len(self) else None) if User is None else self.fromRequireUser(User))
    if habilitys is None:
      return None
    return self._filter(habilitys)
  def random(self, User: utils.Optional[User]=None) -> Hability:
    filter_habilitys = self.filter(User)
    if filter_habilitys is None:
      return None
    habilitys = []
    habilitys += filter_habilitys[0]*20
    habilitys += filter_habilitys[1]*15
    habilitys += filter_habilitys[2]*8
    habilitys += filter_habilitys[3]*4
    return habilitys[randint(0, len(habilitys)-1)]
class _GuildFamilys(GuildElementsFilter):
  def __init__(self, Guild: Guild, /) -> None:
    response = Route.get(f"/desktop/Guilds/{Guild.id}/Family")
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection guild id {self.id} familys")
    super().__init__(Guild, response.json(), Family, newMethod=New_Family)
  def fromUser(self, User: User) -> utils.Optional[list[Family]]:
    familys = [self.get(int(i)) for i in User.familys.toJson()]
    return (familys if len(familys) else None)
  def fromRequireUser(self, User: User) -> utils.Optional[list[Family]]:
    familys = [i for i in self if i.verificationUser(User)]
    return (familys if len(familys) else None)
  def filter(self, User: User=None) -> utils.Optional[dict[int, list[Family]]]:
    familys = ((self if len(self) else None) if User is None else self.fromRequireUser(User))
    if familys is None:
      return None
    return self._filter(familys)
  def random(self, User: User=None) -> utils.Optional[Family]:
    filter_familys = self.filter(User)
    if filter_familys is None:
      return None
    familys = [None]*30
    familys += filter_familys[0]*25
    familys += filter_familys[1]*20
    familys += filter_familys[2]*8
    familys += filter_familys[3]*4
    return familys[randint(0, len(familys)-1)]
class _GuildUsers(GuildElements):
  def __init__(self, Guild: Guild, /) -> None:
    response = Route.get(f"/desktop/Guilds/{Guild.id}/Users")
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection guild id {self.id} users")
    super().__init__(Guild, response.json(), User, newMethod=New_User)
  def fromFamily(self, Family: Family) -> utils.Optional[list[User]]:
    users = [i for i in self if str(Family.id) in i.rolls_familys.toJson()]
    return (users if len(users) else None)
class GuildPlayers(list):
  def __init__(self, Guild: Guild, /) -> None:
    response = Route.get(f"/desktop/Guilds/{Guild.id}/Players")
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection guild id {self.id} players and users")
    players = response.json()
    self.dict = dict(map(lambda elem: (int(elem["id"]), Player(Guild, elem)), players))
    self.ep = Guild
    super().__init__(self.dict.values())
  def get(self, /, id: int) -> utils.Optional[Player]:
    return self.dict.get(id)
  def new(
    self,
    user: User, /,
    *, name: str,
    surname: str=None,
    age: int,
    family: Family
  ) -> Player:
    player = New_Player(
      self.ep,
      user,
      name=name,
      surname=surname,
      age=age,
      family=family
    )
    self.dict[player.id] = player
    self += [player,]
    return player
def New_Guild(
  guild: discord.Guild,
  human: utils.Union[discord.Role, int],
  oni: utils.Union[discord.Role, int],
  hybrid: utils.Union[discord.Role, int],
  separator: list[utils.Union[discord.Role, int]]
) -> Guild: ...