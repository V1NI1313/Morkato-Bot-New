from __future__ import annotations

from .func import Route, setDictOptional
from typing import TYPE_CHECKING
from . import utils
import discord
### -> Exceptions <- ###
from .errors import (
  utilsError,
  GuildNotExists,
  GuildAlreadyExists,
  ResponseError
)

if TYPE_CHECKING:
  from .guild import Guild

Errors = {
  "GuildNotExists": GuildNotExists,
  "GuildAlreadyExists": GuildAlreadyExists
}

class HabilityAlreadyExists(utilsError):
  def __init__(self, hability: Hability ) -> None:
    super().__init__(f"Hability {hability.name} already exists")

class Hability:
  def __init__(
    self,
    Guild: Guild,
    data: dict[str, dict]
  ) -> None:
    self.ep = Guild
    
    self.name: str = data["name"]
    self.id: int = int(data["id"])
    self.roleID: utils.Optional[int] = (int(data["role"]) if not data["role"] is None else None)
    self.rolesID: utils.Optional[list[int]] = ([int(i) for i in data["roles"]] if not data["roles"] is None else None)
    self.rarity: int = data["rarity"]
    self.require: int = data["require"]
    
    self.title: str = data["embed"]["title"]
    self.description: str = data["embed"]["description"]
    self.url: utils.Optional[str] = data["embed"]["url"]
  def __repr__(self) -> str:
    return f"utilz.Hability(name={self.name!r} id={self.id} role={self.role})"
  def __eq__(self, __other: utils.Self) -> bool:
    if not isinstance(__other, Hability):
      raise TypeError("object is not type `utilz.Hability`")
    return __other.id == self.id
  @property
  def role(self) -> utils.Optional[discord.Role]:
    return self.ep._ep.get_role(self.roleID)
  @property
  def roles(self) -> utils.Optional[list[discord.Role]]:
    return list(map(getattr(self.ep._ep, "get_role", lambda id: utils.get(self.ep._ep.roles, id=id)), self.rolesID))
  def get_data(self) -> dict[str, utils.Any]:
    response = Route.get(f"/desktop/Guilds/{self.ep.id}/Hability/{self.id}")
    if not response.status_code == 200:
      raise ResponseError(f"Failed connection in hability id {self.id} of guild id {self.ep.id}")
    return response.json()
  def verificationUser(self, User) -> bool:
    verificationRoles: bool = (self.rolesID is None)
    verificationInventory: bool = (User.rolls_habilitys.toJson().get(str(self.id), 0) < 2)
    if not verificationInventory:
      return False
    if not verificationRoles:
      roles = [i for i in User.auth.roles if i.id in self.rolesID]
      verificationRoles = (len(roles) >= self.require)
      if not verificationRoles:
        return False
    return (verificationRoles and verificationInventory)
  def embed(self, **kwgs) -> discord.Embed:
    title: str = (self.name if self.title is None else self.title.title())
    description: str = (self.description if not self.description is None else "...")
    embed = discord.Embed(
      title=title,
      description=description,
      colour=0x71368A
    )
    if not self.url is None:
      embed.set_image(url=self.url)
    return embed
  def edit(self, **kwgs) -> Hability:
    data = setDictOptional({}, "name", kwgs.get("name"))
    data = setDictOptional(data, "role", kwgs.get("role"))
    data = setDictOptional(data, "roles", kwgs.get("roles"))
    data = setDictOptional(data, "rarity", kwgs.get("rarity"))
    data = setDictOptional(data, "require", kwgs.get("require"))
    
    embed = setDictOptional({}, "title", kwgs.get("embed_title"))
    embed = setDictOptional(embed, "description", kwgs.get("embed_description"))
    embed = setDictOptional(embed, "url", kwgs.get("embed_url"))
    if len(embed):
      data["embed"] = embed
    if not len(data):
      return self
    if "role" in data:
      data["role"] = str((data["role"] if isinstance(data["role"], int) else data["role"].id))
    if "roles" in data:
      for i, item in enumerate(data["roles"]):
        data["roles"][i] = str((item if not isinstance(item, discord.Role) else item.id))
    response = Route.patch(
      f"/desktop/Guilds/{self.ep.id}/Hability/{self.id}",
      data=data,
      headers={
        "content-type": "application/json"
      }
    )
    if not response.status_code == 200:
      raise ResponseError(f"Failed connection in hability id {self.id} of guild id {self.ep.id}")
    return self
def New_Hability(
  Guild: Guild,
  name: str,
  role: discord.Role
) -> Hability:
  _name = name.strip().replace(' ', '-')
  _role = role.id
  
  response = Route.post(
    f"/desktop/Guilds/{Guild.id}/Hability",
    data={
      "name": _name,
      "role": _role
    },
    headers={
      "content-type": "application/json"
    }
  )
  switch = utils.Switch(response.status_code)
  if not switch(200):  
    if switch(402): raise HabilityAlreadyExists(utils.get(Guild.habilitys, role__id=role.id))
    elif switch(404): raise ResponseError(f"failhed connection of guild id {Guild.id}")
  return Hability(
    Guild,
    response.json()
  )