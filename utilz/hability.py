from typing import (Optional, Union, Any)
from .functions import formatstr
import discord

HabilityNew = {"info": {"name": ..., "id": ..., "roles": [], "rarity": 0, "require": 1}, "content": {"title": str(...), "description": str(...), "url": str(...)}, "status": {"damege": {"type": "*", "value": 1}, "stamina": {"type": "*", "value": 1}}}

class Hability:
    def __init__(self, Guild: Any, Name: str) -> None:
        HabilityInfo: dict[str, Any] = Guild._habilitys[Name]
        self._name = Name
        
        self.name = HabilityInfo["info"]["name"]
        self.rarity = HabilityInfo["info"]["rarity"]
        self.require = HabilityInfo["info"]["require"]
        self.role: discord.Role = Guild.disGuild.get_role(int(HabilityInfo["info"]["id"]))
        self.roles: list[discord.Role] = [Guild.disGuild.get_role(int(i)) for i in HabilityInfo["info"]["roles"]]
        self._status: dict[str, Any] = HabilityInfo["status"]
        self._info: dict[str, Any] = HabilityInfo["content"]
        self.guild = Guild

        self.info: _HabilityInfo = _HabilityInfo(self)
    def __repr__(self) -> str: return str("utilz.Hability(Guild={guild!r}, Name={habi!r})".format(guild=str(self.guild), habi=str(self.name)))
    def __str__(self) -> str: return self.__repr__()
    def __eq__(self, __ob) -> bool: return self.role == __ob.role
    def embed(self, **kwargs) -> discord.Embed:
        name = str(self.name[0].title() + self.name[1:]).replace('-', ' ')
        title = str(kwargs.get('title', self.info.title if not self.info.title is None else name))
        _title = str(title[0].title() + title[1:])
        title = str(title[0].title() + title.lower()[1:])
        description = kwargs.get('description', self.info.description)
        url = kwargs.get('url', self.info.url)
        embed = discord.Embed(
            title=str(_title).replace('-', ' '),
            description=formatstr(str(description if not description is None else "No description"), name=str(name), title=str(title)),
            colour=0x71368A
        )
        if not url is None: embed.set_image(url=str(url))
        return embed
    def add_role(self, require: int=None, *roles: tuple[discord.Role]) -> None:
        self.require = require if not require is None else self.require
        self.roles += list(roles)
        self.refresh()
    def refresh(self) -> None:
        self.guild._habilitys[self.name] = {"info": {"name": self.name, "id": self.role.id, "roles": [i.id for i in self.roles], "rarity": self.rarity, "require": self.require}, "content": self._info, "status": self._status}
        self.guild.save_all()
        self.__init__(self.guild, self._name)
    def VerificationRequirePlayer(self, player: Any) -> bool:
        if not len(self.roles): return True
        require = int(self.require)
        for i in self.roles:
            if i in player.User.roles:
                require -= 1
            if require == 0: return True
        return False
    def edit(self, **kwargs) -> None:
        return self.info.edit(**kwargs)
class _HabilityInfo:
    def __init__(self, Hability: Hability) -> None:
        self.Hability = Hability
    @property
    def title(self) -> Optional[str]: return self.Hability._info["title"]
    @title.setter
    def title(self, __value: Any) -> None:
        if not isinstance(__value, str) or not __value is None:
            raise TypeError("Suport to `str` not {type!r}".format(type=type(__value).__name__))
        self._title = __value
        self.Hability._info["title"] = __value
    @property
    def description(self) -> Optional[str]: return self.Hability._info["description"]
    @description.setter
    def description(self, __value: Any) -> None:
        if not isinstance(__value, str) or not __value is None:
            raise TypeError("Suport to `str` not {type!r}".format(type=type(__value).__name__))
        self._description = __value
        self.Hability._info["description"] = __value
    @property
    def url(self) -> Optional[str]: return self.Hability._info["url"]
    @url.setter
    def url(self, __value: Any) -> None:
        if not isinstance(__value, str) or not __value is None:
            raise TypeError("Suport to `str` not {type!r}".format(type=type(__value).__name__))
        self._url = __value
        self.Hability._info["url"] = __value
    def edit(self, **kwargs) -> None:
        self.Hability._info["title"] = kwargs.get('title', self.title)
        self.Hability._info["description"] = kwargs.get('description', self.description)
        self.Hability._info["url"] = kwargs.get('url', self.url)
        self.Hability.refresh()
def New_Hability(
    Guild: Any,
    Name: str,
    role: Union[discord.Role, int],
    **kwargs
) -> Hability:
    HabilityNew["info"]["name"] = Name
    HabilityNew["info"]["id"] = int(role if isinstance(role, int) else role.id)
    HabilityNew["info"]["roles"] = kwargs.get('roles', [])
    HabilityNew["content"]["title"] = kwargs.get('title', None)
    HabilityNew["content"]["description"] = kwargs.get('description', None)
    HabilityNew["content"]["url"] = kwargs.get('url', None)

    Guild._habilitys[Name] = HabilityNew
    Guild.save_all()
    return Hability(
        Guild,
        Name
    )