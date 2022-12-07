from typing import (Optional, Union, Any)
from .func import Route
import discord

FamilyErrors = {}

class Family:
  def __init__(
    self,
    Guild: Any,
    data: dict[str, dict]
  ) -> None:
    self.ep = Guild
    
    self.name: str = data["info"]["name"]
    self.id: int = data["info"]["id"]
    self.roleID: Optional[int] = data["info"]["role"]
  def __repr__(self) -> str:
    return f"utilz.Family(name={self.name!r} id={self.id} role={self.role})"
  def __eq__(self, __other: Union[discord.Role, str, int]) -> bool:
    if isinstance(__other, Family):
      return __other.id == self.id
    __other = (__other if not isinstance(__other, discord.Role) else __other.id)
    return (
      __other == self.name
      or __other == self.id
      or (
        not self.roleID is None
        and self.roleID == __other
      )
    )
  @property
  def role(self) -> Optional[discord.Role]:
    return self.ep._ep.get_role(self.roleID)
  def get_data(self) -> dict[str, dict]:
    response = Route.get(f"/desktop/Guilds/{self.ep.id}/Family/{self.id}")
    if not response.status_code == 200:
      raise FamilyErrors.get(response.json()["message"], Exception)(self.ep, self.name)
    return response.json()
  def edit(self, **kwgs) -> None: ...
def New_Family(
  Guild: Any,
  name: str,
  role: Union[discord.Role, int]
) -> Family:
  response = Route.post(
    f"/desktop/Guilds/{Guild.id}/Family",
    data={
      "name": name,
      "role": (role if isinstance(role, int) else role.id)
    },
    headers={
      "content-type": "application/json"
    }
  )
  if not response == 200:
    raise FamilyErrors.get(response.json()["message"], Exception)(Guild, name)
  return Family(
    Guild=Guild,
    data=response.json()
  )