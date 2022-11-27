from typing import (Optional, Union, Any)
from .func import Route
import discord
### -> Exceptions <- ###
from .errors import (
  GuildNotExists,
  GuildAlreadyExists
)

GuildErrors = {
  "GuildNotExists": GuildNotExists,
  "GuildAlreadyExists": GuildAlreadyExists
}

class Guild:
  def __init__(
    self,
    Guild: discord.Guild,
    data: dict[str, Any]
  ) -> None:
    self._ep = Guild
    self.data = data
  @property
  def config(self):
    return _GuildConfig(self)
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
    data = self.config.edit(**kwgs)
    self.__init__(self, data)
  @classmethod
  def from_guild(
    cls,
    _Guild: discord.Guild
  ):
    response = Route.get(f"/desktop/Guilds/{_Guild.id}")
    if not response.status_code == 200:
      raise GuildErrors.get(response.json()["message"], Exception)(_Guild)
    return cls(
      Guild=_Guild,
      data=response.json()
    )
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