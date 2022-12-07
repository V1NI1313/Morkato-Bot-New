from typing import (Optional, Union, Any)
from typing_extensions import (Self)
from functools import cache
from .func import Route
import discord
### -> Exceptions <- ###
from .errors import (
  GuildNotExists,
  GuildAlreadyExists,
  ResponseError
)

GuildErrors = {
  "GuildNotExists": GuildNotExists,
  "GuildAlreadyExists": GuildAlreadyExists
}
HabilityErrors = {
  
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
class Hability:
  def __init__(
    self,
    Guild: Any,
    data: dict[str, dict]
  ) -> None:
    self.ep = Guild
    
    self.name: str = data["name"]
    self.id: int = int(data["id"])
    self.roleID: Optional[int] = data["role"]
    if not self.roleID is None:
      self.roleID = int(self.roleID)
    self.title: str = data["embed"]["title"]
    self.description: str = data["embed"]["description"]
    self.url: Optional[str] = data["embed"]["url"]
  def __repr__(self) -> str:
    return f"utilz.Hability(name={self.name!r} id={self.id} role={self.roleID})"
  def __eq__(self, __other: Union[discord.Role, str, int]) -> bool:
    if isinstance(__other, discord.Role):
      return not self.roleID is None and self.role.id == __other.id
    if isinstance(__other, Hability):
      __other = __other.id
    return ((
        isinstance(__other, str)
        and __other == self.name
      ) or (
        isinstance(__other, int)
        and self.id == __other
      ))
  @property
  def role(self) -> Optional[discord.Role]:
    return self.ep._ep.get_role(self.roleID)
  def get_data(self) -> dict[str, Any]:
    response = Route.get(f"/desktop/Guilds/{self.ep.id}/Hability/{self.id}")
    if not response.status_code == 200:
      raise ResponseError(f"Failed connection in hability id {self.id} of guild id {self.ep.id}")
    return response.json()
  def embed(self, **kwgs) -> discord.Embed:
    title: str = (self.name if self.title is None else self.title.title())
    description: str = (self.description if not self.description is None else "...")
    embed = discord.Embed(
      title=title,
      description=f"{description}\n\n**✦ ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ・あ・⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ✦**",
      colour=0x71368A
    )
    if not self.url is None:
      embed.set_image(url=self.url)
    return embed
  def edit(self, **kwgs) -> Self:
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
      return
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
  Guild: Any,
  name: str,
  role: Union[discord.Role, int]
) -> Hability:
  _name = name.strip().replace(' ', '-')
  _role = (role if isinstance(role, int) or role is None else role.id)
  
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
  if not response.status_code == 200:
    raise HabilityErrors.get(response.json()["message"], Exception)(name)
  return Hability(
    Guild,
    response.json()
  )