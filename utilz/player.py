from typing import (Optional, Union, Any)
from functools import cache
from typing_extensions import (Self)
from .user import User
from .func import Route
import discord

PlayerErrors = {}

class Player(User):
  def __init__(
    self,
    Guild,
    data: dict[str, dict]
  ) -> None: super().__init__(Guild, data)
  def __repr__(self) -> str: ...
  def __eq__(self) -> bool: ...
  @property
  @cache
  def settings(self): ...
  def edit(self, **kwgs) -> None: ...
def New_Player(
  Guild: discord.Guild,
  User: Union[discord.User, discord.Member],
  name: str,
  surname: str,
  age: int
) -> Player: ...