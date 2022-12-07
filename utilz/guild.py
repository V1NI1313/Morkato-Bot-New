from .hability import (Hability, New_Hability)
from typing import (Optional, Generic, Callable, TypeVar, Union, Any)
from typing_extensions import (Self)
from .user import (User, New_User)
from .family import (Family, New_Family)
from .player import (Player, New_Player)
from functools import cache
from .func import Route
import discord
### -> Exceptions <- ###
from .errors import (
  utilsError,
  GuildNotExists,
  GuildAlreadyExists,
  FamilyNotExists,
  HabilityNotExists,
  PlayerNotExists,
  UserNotExists
)

GuildErrors = {
  "GuildNotExists": GuildNotExists,
  "GuildAlreadyExists": GuildAlreadyExists
}
T = TypeVar('T')
class Guild:
  def __init__(
    self,
    Guild: discord.Guild,
    data: dict[str, Any]
  ) -> None:
    self._ep = Guild
    self.data = data
    self.id = Guild.id
    
    self.human_roleID: Optional[int] = data["roles"]["human"]
    self.oni_roleID: Optional[int] = data["roles"]["oni"]
    self.hybrid_roleID: Optional[int] = data["roles"]["hybrid"]
  @property
  def human_role(self) -> Optional[discord.Role]:
    return self._ep.get_role(self.human_roleID)
  @property
  def oni_role(self) -> Optional[discord.Role]:
    return self._ep.get_role(self.oni_roleID)
  @property
  def hybrid_role(self) -> Optional[discord.Role]:
    return self._ep.get_role(self.hybrid_roleID)
  @property
  @cache
  def settings(self):
    return _GuildConfig(self)
  @property
  @cache
  def habilitys(self):
    return _GuildHabilitys(self)
  @property
  @cache
  def familys(self):
    return _GuildFamilys(self)
  @property
  @cache
  def players(self):
    return _GuildPlayers(self)
  @property
  @cache
  def users(self):
    return _GuildUsers(self)
  def edit(self, **kwgs) -> None:
    data = self.data
    roles = data["roles"]
    player = data["player"]
    roles["human"] = (
      kwgs.get("human_role", roles["human"]) 
      if isinstance(kwgs.get("human_role", roles["human"]), int)
      else kwgs.get("human_role", roles["human"]).id
    )
    roles["oni"] = (
      kwgs.get("oni_role", roles["oni"]) 
      if isinstance(kwgs.get("oni_role", roles["oni"]), int)
      else kwgs.get("oni_role", roles["oni"]).id
    )
    roles["hybrid"] = (
      kwgs.get("hybrid_role", roles["hybrid"]) 
      if isinstance(kwgs.get("hybrid_role", roles["hybrid"]), int)
      else kwgs.get("hybrid_role", roles["hybrid"]).id
    )
    player["defaultStatus"]["human"] = {
      "life": kwgs.get("human_life", player["defaultStatus"]["human"]["life"]),
      "stamina": kwgs.get("human_stamina", player["defaultStatus"]["human"]["stamina"])
    }
    player["defaultStatus"]["oni"] = {
      "life": kwgs.get("oni_life", player["defaultStatus"]["oni"]["life"]),
      "stamina": kwgs.get("oni_stamina", player["defaultStatus"]["oni"]["stamina"])
    }
    player["defaultStatus"]["hybrid"] = {
      "life": kwgs.get("hybrid_life", player["defaultStatus"]["hybrid"]["life"]),
      "stamina": kwgs.get("hybrid_stamina", player["defaultStatus"]["hybrid"]["stamina"])
    }
    player["rolls"] = {
      "family": kwgs.get("family_rolls", player["rolls"]["family"]),
      "hability": kwgs.get("hability_rolls", player["rolls"]["hability"])
    }
    data = self.settings.edit(**kwgs)
    self.__init__(self, data)
  @classmethod
  def from_guild(
    cls,
    _Guild: discord.Guild
  ) -> Self:
    response = Route.get(f"/desktop/Guilds/{_Guild.id}")
    if not response.status_code == 200:
      raise GuildErrors.get(response.json()["message"], Exception)(_Guild)
    return cls(
      Guild=_Guild,
      data=response.json()
    )
class _GuildUsers(list):
  def __init__(self, Guild: Guild) -> None:
    self.ep = Guild
    response = Route.get(f"/desktop/Guilds/{Guild.id}/Users")
    if not response.status_code == 200:
      raise GuildErrors.get(response.json()["message"], utilsError)(Guild)
    data = response.json()
    for i in data:
      self.append(User(self.ep, i))
  def get(
    self,
    arg: Union[discord.Member, User]
  ) -> User:
    try: return self[self.index(arg)]
    except: raise UserNotExists(self.ep, arg)
  def new(
    self,
    _User: Union[discord.Member, discord.User]
  ) -> User:
    user = New_User(self.ep, _User)
    self.append(user)
    return user
class _GuildPlayers(list):
  def __init__(self, Guild: Guild) -> None:
    self.ep = Guild
    response = Route.get(f"/desktop/Guilds/{Guild.id}/Players")
    if not response.status_code == 200:
      raise GuildErrors.get(response.json()["message"])(Guild)
    data = response.json()
    for i in data:
      self.append(Player(Guild, i))
  def get(
    self,
    arg: Union[Player, int]
  ) -> Player:
    try: return self[self.index(arg)]
    except: raise PlayerNotExists(arg)
class _GuildFamilys(list):
  def __init__(self, Guild: Guild) -> None:
    self.ep = Guild
    response = Route.get(f"/desktop/Guilds/{Guild.id}/Family")
    if not response.status_code == 200:
      raise GuildErrors.get(response.json()["message"])(Guild)
    data = response.json()
    for i in data:
      self.append(Family(Guild, i))
  def get(
    self,
    arg: Union[discord.Role, str, int]
  ) -> Family:
    try: return self[self.index(arg)]
    except: raise FamilyNotExists(arg)
  def new(
    self,
    name: str,
    role: Union[discord.Role, int]
  ) -> Family: ...
class _GuildHabilitys(list):
  def __init__(self, Guild: Guild) -> None:
    self.ep = Guild
    response = Route.get(f"/desktop/Guilds/{Guild.id}/Hability")
    if not response.status_code == 200:
      raise GuildErrors.get(response.json()["message"])(Guild)
    data = response.json()
    for i in data:
      self.append(Hability(Guild, i))
  def get(
    self,
    arg: Union[discord.Role, str, int]
  ) -> Hability:
    try: return self[self.index(arg)]
    except: raise HabilityNotExists(arg)
  def new(
    self,
    name: str,
    role: Optional[discord.Role]=None
  ) -> Hability:
    hability = New_Hability(self.ep, name, role)
    self.append(hability)
    return hability
class _GuildConfig:
  def __init__(self, Guild: Guild) -> None:
    self.ep = Guild
  def edit(self, **kwgs) -> None:
    response = Route.patch(
      f"/desktop/Guilds/{self.ep._ep.id}",
      data=self.ep.data,
      headers={
        "content-type": "application/json"
      }
    )
    if not response.status_code == 200:
      raise GuildErrors.get(response.json()["message"], Exception)(self.ep)
    return response.json()
def New_Guild(
  _Guild: discord.Guild,
  human: Union[discord.Role, int],
  oni: Union[discord.Role, int],
  hybrid: Union[discord.Role, int],
  separator: list[Union[discord.Role, int]]
) -> Guild:
  data = {
    "human": (human if isinstance(human, int) else human.id),
    "oni": (oni if isinstance(oni, int) else oni.id),
    "hybrid": (hybrid if isinstance(hybrid, int) else hybrid.id),
    "separator": [(i if isinstance(i, int) else i.id) for i in separator if (isinstance(i, int) or isinstance(i, discord.Role))]
  }
  response = Route.post(
    f"/desktop/Guilds/{_Guild.id}",
    data=data,
    headers={
      "content-type": "application/json"
    }  
  )
  if not response.status_code == 200:
    raise GuildErrors.get(response.json()["message"], Exception)(_Guild)
  return Guild(
    Guild=_Guild,
    data=response.json()
  )