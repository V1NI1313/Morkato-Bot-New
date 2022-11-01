__slots__ = [
    "Player",
    "New_Player"
]

from .errors import PlayerMappedBreed
from typing import (Optional, Any)
from .hability import Hability
from .family import Family
import discord
import json
import os

PlayerNew = {"info": {"name": ..., "xp": 0, "level": 1, "lvMin": 100}, "status": {"life": 3000, "stamina": 3000, "force": 0.5}, "historic": {}}
class _PlayerHistoric: ...
class Player:
    def __init__(self, Guild: Any, id: str) -> None:
        self.Guild = Guild
        self.User: discord.Member = Guild.disGuild.get_member(int(id))

        self.habilitys: Optional[list[Hability]] = Guild.habilitys.getforPlayer(self)
        self.family: Optional[Family] = Guild.familys.getforPlayer(self)
    def __repr__(self) -> str: return str("utilz.Player(Guild={guild!r}, user={id!r})".format(guild=str(self.Guild), id=str(self.User)))
    def __str__(self) -> str: return self.__repr__()
def New_Player(
    Guild: Any,
    Member: discord.Member,
    Name: str,
    **kwargs
) -> Player:
    PlayerNew["info"]["name"] = Name
    if (
        Guild.disGuild.get_role(1031641341198864394) in Member.roles 
        and not Guild.disGuild.get_role(1031641613883146280) in Member.roles
        and not Guild.disGuild.get_role(1031642887374508042) in Member.roles
    ): PlayerNew["info"]["breed"] = "human"
    elif (
        Guild.disGuild.get_role(1031641613883146280) in Member.roles
        and not Guild.disGuild.get_role(1031641341198864394) in Member.roles
        and not Guild.disGuild.get_role(1031642887374508042) in Member.roles
    ): PlayerNew["info"]["breed"] = "oni"
    elif (
        Guild.disGuild.get_role(1031642887374508042)
        and not Guild.disGuild.get_role(1031641613883146280) in Member.roles
        and not Guild.disGuild.get_role(1031641341198864394) in Member.roles

    ): PlayerNew["info"]["breed"] = "hybrid"
    else: raise PlayerMappedBreed(Member)

    Guild._players[str(Member.id)] = PlayerNew
    Guild.save_all()
    return Player(
        Guild,
        str(Member.id),
        playerIni=PlayerNew
    )