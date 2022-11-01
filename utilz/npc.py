from numerize.numerize import numerize as num_fmt
from typing import (Union, Optional, Any)
from .player import Player
import requests
import discord
import json
import os
### -> Exceptions <- ###
from .errors import NpcNotFound

_dir = './Json/Npc' if not __name__ == '__main__' else '../Json/Npc'
NpcNew = {'config': {"player": ..., "historic": []}, 'IniStatus': {"hearth": 1000, "stamina": 1000}, 'status': {"hearth": 1000, "stamina": 1000}, 'info-user': {"nick": ..., "url": None, "card": {"description": None, "url": None, "history": None}, "roles": []}}

class _InfoNpc:
    def __init__(self, InfoNpc: dict[str, Any]) -> None:
        self._InfoNpc = InfoNpc
    def __repr__(self) -> str:
        return self.nick
    @property
    def nick(self): return self._InfoNpc["nick"]
    @nick.setter
    def nick(self, __value: Any) -> None:
        if not isinstance(__value, str):
            raise TypeError("object value `{type}` not suported, support type to `str`!".format(type=str(type(__value))))
        self._nick = __value
        self._InfoNpc["nick"] = __value
    @property
    def url(self): return self._InfoNpc["url"]
    @url.setter
    def url(self, __value: Any) -> None:
        if not isinstance(__value, str) or not __value is None:
            raise TypeError("object value `{type}` not suported, support type to `str and link`!".format(type=str(type(__value))))
        self._url = None if __value is None else requests.get(url=__value).url
        self._InfoNpc["url"] = __value
    @property
    def history(self): return self._InfoNpc["card"]["history"]
    @history.setter
    def history(self, __value: Any) -> None:
        if not isinstance(__value, str):
            raise TypeError("object value `{type}` not suported, support type to `str`!".format(type=str(type(__value))))
        self._history = __value
        self._InfoNpc["card"]["history"] = __value
    @property
    def roles(self): return self._InfoNpc["roles"]
    def card(self, guild: discord.Guild) -> discord.Embed:
        embed = discord.Embed(
            title='Info-Npc',
            description='**`{npc} user info`\n\nHistória - `{history}`**'.format(npc=str(self), history=str(self.history if not self.history == None else 'No History')),
            colour=0x71368A
        )
        # if not self.url is None: embed.set_image(url=self.url)
        embed.set_thumbnail(url=self.url)
        if not len(self.roles) == 0:
            embed.add_field(name='Cargos', value='**`{roles}`**'.format(roles='\n'.join([str(guild.get_role(i)) for i in self.roles])), inline=False)
        return embed
class Npc:
    fmtDirectory: Optional[str]
    Name: Optional[str]
    def __init__(self, Name: str, chr: Union[Union[str, bytes], dict[str, bytes]]=_dir) -> None:
        self.Name = str(Name)
        if isinstance(chr, str) or isinstance(chr, bytes):
            self.fmtDirectory: str = os.path.join(str(chr if isinstance(chr, str) else chr.decode('utf8')), Name+'.json').replace('\\', '/')
            try:
                with open(os.path.join(self.fmtDirectory), 'r', encoding='utf8') as a:
                    chr = json.load(a)
            except FileNotFoundError: raise NpcNotFound(str(self.Name))
        self._conflip: dict[str, Any] = chr
        self._info: dict[str, Any] = self._conflip['info-user']
        self._config: dict[str, Any] = self._conflip['config']
        self._status: dict[str, Any] = self._conflip['status']
        self._IniStatus: dict[str, Any] = self._conflip['IniStatus']
    def __repr__(self) -> str:
        return self.Name
    @property
    def info(self): return _InfoNpc(self._info)
    @property
    def hearth(self): return self._status["hearth"]
    @hearth.setter
    def hearth(self, __value: Any) -> None:
        if not isinstance(__value, int):
            raise TypeError("object value {type} not suported, support type to `int`!".format(type=str(type(__value))))
        self._hearth: int = __value if __value > 0 or __value is None else -1
        self._status["hearth"] = __value if __value > 0 or __value is None else -1
    @property
    def stamina(self): return self._status["stamina"]
    @stamina.setter
    def stamina(self, __value: Any) -> None:
        if not isinstance(__value, int):
            raise TypeError("object value {type} not suported, support type to `int`!".format(type=str(type(__value))))
        self._stamina: int = __value if __value > 0 or __value is None else 1
        self._status["stamina"] = __value if __value > 0 or __value is None else 1
    @property
    def IniHearth(self): return self._IniStatus["hearth"]
    @IniHearth.setter
    def IniHearth(self, __value: Any) -> None:
        if not isinstance(__value, int):
            raise TypeError("object value {type} not suported, support type to `int`!".format(type=str(type(__value))))
        self._IniHearth: int = __value if __value > 0 else 1
        self.hearth = self._IniHearth        
        self._IniStatus["hearth"] = self._IniHearth
    @property
    def IniStamina(self): return self._IniStatus["stamina"]
    @IniStamina.setter
    def IniStamina(self, __value: Any) -> None:
        if not isinstance(__value, int):
            raise TypeError("object value {type} not suported, support type to `int`!".format(type=str(type(__value))))
        self._IniStamina: int = __value if __value > 0 else 1
        self.stamina = self._IniStamina
        self._IniStatus["stamina"] = self._IniStamina
    @property
    def player(self): return Player(self._config["player"])
    async def get_webhook(self, channel: discord.TextChannel, ShowStatus: bool=True) -> discord.Webhook:
        text: str = str("{name} | ❤️ {life} | 💨 {stamina}".format(name=str(self), life=str(num_fmt(self.hearth)), stamina=str(num_fmt(self.stamina)))) if ShowStatus else str(self)
        url: Optional[bytes] = None if self.info.url is None else requests.get(url=self.info.url).content
        return await channel.create_webhook(name=text, avatar=url)
    def save_all(self) -> None:
        conflip = {
            'config': self._config, 
            'IniStatus': self._IniStatus,
            'status': self._status,
            'info-user': self.info._InfoNpc
        }
        with open(os.path.join(self.fmtDirectory), 'w') as a:
            json.dump(conflip, a, indent=2)
def New_Npc(
    Name: str, 
    player: Player,
    roles: list[Union[discord.Role, int]]=None,
    directory: Union[str, bytes]=_dir
    ) -> Npc:
    NpcNew['config']['roles'] = [] if roles is None else [int(i if isinstance(i, int) else i.id) for i in roles]
    NpcNew['info-user']['nick'] = Name
    NpcNew['config']['player'] = str(player.User.id)
    with open(os.path.join(directory, Name+'.json'), 'w') as a:
        json.dump(NpcNew, a, indent=2)
    return Npc(Name=Name, chr=NpcNew)
def all_npcsPlayer(Player: Player) -> list[Npc]: ...
def all_npcsDirectory(directory: Union[str, bytes]) -> list[Npc]: ...
