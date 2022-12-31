from __future__ import annotations

from .func import Route, setDictOptional
from typing import TYPE_CHECKING
from . import utils
import discord
### -> Exceptions <- ###
from .errors import (
  utilsError,
  ResponseError
)

if TYPE_CHECKING:
  from .guild import Guild

def fixData(data: dict) -> dict:
  if "role" in data:
    data["role"] = str(data["role"].id if isinstance(data["role"], discord.Role) else data["role"])
  if "roles" in data:
    for i, item in enumerate(data["roles"]):
      data["roles"][i] = str(item.id if isinstance(item, discord.Role) else item)
  if "habilitys" in data:
    data["habilitys"] = [str(i.id) for i in data["habilitys"]]
  return data

class FamilyAlreadyExists(utilsError):
  def __init__(self, family: Family) -> None:
    super().__init__(f"Family id  {family.id} already exists!")
class Family:
  def __init__(
    self,
    Guild: Guild,
    data: dict[str, dict]
  ) -> None:
    self.ep = Guild
    
    self.name: str = data["name"]
    self.id: int = int(data["id"])
    self.roleID: utils.Optional[int] = int(data["role"])
    self.rolesID: utils.Optional[list[int]] = [int(i) for i in data["roles"]]
    self.limit: utils.Optional[int] = data["limit"]
    self.require: int = data["require"]
    self.rarity: int = data["rarity"]
    self.embed_title: str = data["embed"]["title"]
    self.embed_description: str = data["embed"]["description"]
    self.embed_image: utils.Optional[str] = data["embed"]["url"]
  def __repr__(self) -> str:
    return f"utilz.Family(name={self.name!r} id={self.id} role={self.role})"
  def __eq__(self, __other: utils.Union[discord.Role, str, int]) -> bool:
    if isinstance(__other, Family):
      return self.id == __other.id
    __other = (__other.id if isinstance(__other, discord.Role) else __other)
    if not isinstance(__other, str) and not isinstance(__other, int):
      return False
    return (
      __other == self.roleID
      or __other == self.id
      or __other == self.name
    )
  @property
  def role(self) -> utils.Optional[discord.Role]:
    return self.ep._ep.get_role(self.roleID)
  @property
  def roles(self) -> utils.Optional[list[discord.Role]]:
    return (None if self.rolesID is None else [self.ep._ep.get_role(i) for i in self.roleID])
  def get_data(self) -> dict[str, dict]:
    response = Route.get(f"/desktop/Guilds/{self.ep.id}/Family/{self.id}")
    if not response.status_code == 200:
      raise ResponseError(f"Failhed connection family id {self.id} of guild id {self.ep.id}")
    return response.json()
  def verificationUser(self, User) -> bool:
    verificationLimit = (self.limit is None)
    verificationRoles = bool(len(self.rolesID))
    verificationInventory = User.rolls_familys.toJson().get(str(self.id), 0) < 3
    if not verificationInventory:
      return False
    if not verificationLimit:
      players = self.ep.users.fromFamily(self)
      verificationLimit = (players is None or not len(players) >= self.limit)
      if not verificationLimit:
        return False
    if not verificationRoles:
      roles = [i for i in User.auth.roles if i.id in self.rolesID]
      verificationRoles = len(roles) >= self.require
      if not verificationRoles:
        return False
    return (verificationLimit and verificationRoles and verificationInventory)
  def embed(self, **kwgs) -> discord.Embed:
    title: str = kwgs.get("title", self.embed_title)
    description: str = kwgs.get("description", self.embed_description)
    url: str = kwgs.get("url", self.embed_image)
    embed = discord.Embed(
      title=title,
      description=description,
      color=0x71368A
    )
    if not url is None:
      embed.set_image(url=url)
    return embed
  def edit(self, **kwgs) -> Family: 
    data = setDictOptional({}, "name", kwgs.get("name"))
    data = setDictOptional(data, "role", kwgs.get("role"))
    data = setDictOptional(data, "roles", kwgs.get("roles"))
    data = setDictOptional(data, "habilitys", kwgs.get("habilitys"))
    data = setDictOptional(data, "rarity", kwgs.get("rarity"))
    data = setDictOptional(data, "require", kwgs.get("require"))
    data = setDictOptional(data, "limit", kwgs.get("limit"))
    embed = setDictOptional({}, "title", kwgs.get("embed_title"))
    embed = setDictOptional(embed, "description", kwgs.get("embed_description"))
    embed = setDictOptional(embed, "url", kwgs.get("embed_url"))
    message = setDictOptional({}, "content", kwgs.get("message_content"))
    message = setDictOptional(message, "url", kwgs.get("message_url"))
    if len(embed):
      data["embed"] = embed
    if len(message):
      data["message"] = message
    if not len(data):
      return self
    response = Route.patch(
      f"/desktop/Guilds/{self.ep.id}/Family/{self.id}",
      data=fixData(data),
      headers={
        "content-type": "application/json"
      }
    )
    if not response.status_code == 200:
      raise ResponseError(f"Failed connection in family id {self.id} of guild id {self.ep.id}")
    self.__init__(self.ep, response.json())
    return self
def New_Family(
  Guild: Guild,
  name: str,
  role: discord.Role,
  **kwgs
) -> Family:
  response = Route.post(
    f"/desktop/Guilds/{Guild.id}/Family",
    data=fixData({
      "name": name,
      "role": str(role.id)
    }),
    headers={
      "content-type": "application/json"
    }
  ); switch = utils.Switch(response.status_code)
  if switch(404):
    raise ResponseError(f"Failhed connection of guild id {Guild.id}")
  return Family(
    Guild=Guild,
    data=response.json()
  ).edit(**kwgs)