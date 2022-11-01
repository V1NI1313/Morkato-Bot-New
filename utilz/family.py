from .functions import endswith, formatstr
from typing import (Optional, Union, Any)
from .hability import Hability
import discord
### - > Exceptions <- ###
from .errors import HabilityNotFound

class Family:
    def __init__(
        self,
        Guild: Any,
        Name: str,
    ) -> None:
        conflip: dict[str, Any] = Guild._familys[Name]
        self.Guild: discord.Guild = Guild.disGuild
        self.name = Name
        self.ep = Guild

        self._config: dict[str, Union[str, int]] = conflip["info"]
        self._info: dict[str, Optional[str]] = conflip["content"]
        self._habilitys: list[int] = self._config["habilitys"]
        self.message = conflip["message"]

        self.roles: list[discord.Role] = [self.Guild.get_role(i) for i in self._config["roles"]]
        self.habilitys: _FamilyHabilitys[str, Hability] = _FamilyHabilitys(Guild, self)
        self.role: discord.Role = self.Guild.get_role(self._config["id"])
        self.info: _InfoFamily = _InfoFamily(self)

        self.content: Optional[str] = self.message["content"]
        self.file: Optional[Union[bytes, str, int]] = self.message["file"]

        self.rarity: int = self._config["rarity"]
        self.require: int = self._config["require"]
        self.limit: Optional[int] = self._config["limit"]
    def __eq__(self, __key: Any) -> bool:
        return self.role.id == __key.role.id
    def refresh(self) -> None:
        self._config["habilitys"] = self._habilitys
        self._config["rarity"] = self.rarity
        self._config["id"] = self.role.id

        conflip = {"info": self._config, "content": self._info, "message": self.message}
        self.ep._familys[self.name] = conflip
        self.ep.save_all()
    def embed(self, **kwgs) -> discord.Embed:
        title: str = str(kwgs.get('title', self.info.title))
        title = "{0}{1}".format(title[0].title(), title[1:])
        description: str = str(kwgs.get('description', self.info.description))
        url: Optional[str] = kwgs.get('url', self.info.url)

        embed = discord.Embed(
            title=title,
            description=formatstr(description, title=title),
            colour=0x71368A
        )
        if not url is None:
            embed.set_image(url=url)
        return embed
    def VerificationRequirePlayer(self, player: Any) -> bool:
        if not len(self.roles) and self.limit is None: return True
        verificationRole = not bool(len(self.roles))
        verificationLimit = self.limit is None
        require = int(self.require)
        if not verificationRole:
            for i in self.roles:
                if i in player.User.roles:
                    require -= 1
                if require == 0:
                    verificationRole = True
                    break
        players = self.ep.players.getfromFamily(self)
        if not verificationLimit and not int(0 if players is None else len(players)) == self.limit:
            verificationLimit = True
        return (verificationRole and verificationLimit)
    def edit(self, **kwgs) -> None:
        self.rarity = kwgs.get('rarity', self.rarity)
        self.message["content"] = kwgs.get('content', self.content)
        self.message["file"] = kwgs.get('file', self.file)
        self.info.edit(**kwgs)
        self.__init__(self.ep, self.name)
FamilyNew = {"info": {"name": str, "id": int, "habilitys": list[int], "roles": [], "rarity": int, "require": 1, "limit": None}, "content": {"title": Optional[str], "description": Optional[str], "url": Optional[str]}, "message": {"content": Optional[str], "file": Optional[str]}}
class _FamilyHabilitys(dict):
    def __init__(self, Guild: Any, family: Family) -> None:
        habilitys = {}
        for i in family._habilitys:
            Hability = Guild.habilitys.get(i)
            habilitys[Hability.name] = Hability
        super().__init__(habilitys)
        self.Guild = Guild
        self._ep = family
    def add(self, *arg: tuple[Union[discord.Role, str, int]]) -> list[Hability]:
        _Habilitys = []
        for i in arg:
            try:
                Habi: Hability = self.Guild.habilitys.get(i)
                self._ep._habilitys.append(Habi.role.id)
                self[Habi.name] = Habi
                _Habilitys.append(Habi)
            except HabilityNotFound: ...
        self._ep.refresh()
        return _Habilitys
    def get(self, arg: Union[discord.Role, str, int]) -> None:
        for i in self.values():
            if ((
                isinstance(arg, discord.Role) or isinstance(arg, int)
                ) and i.role.id == int(arg if isinstance(arg, int) else arg.id)): return i
            elif i.name  == str(arg): return i
        raise HabilityNotFound(str(arg))
class _InfoFamily:
    def __init__(self, family: Family) -> None:
        self._ep = family
    @property
    def title(self) -> Optional[str]: return self._ep._info["title"]
    @title.setter
    def title(self, __value: Any) -> None:
        if not isinstance(__value, str) or not __value is None:
            raise TypeError("support to \'str\' not {type!r}".format(type=type(__value).__name__))
        self._ep._info["title"] = __value
    @property
    def description(self) -> Optional[str]: return self._ep._info["description"]
    @description.setter
    def description(self, __value: Any) -> None:
        if not isinstance(__value, str) or not __value is None:
            raise TypeError("support to \'str\' not {type!r}".format(type=type(__value).__name__))
        self._ep._info["description"]
    @property
    def url(self) -> Optional[str]: return self._ep._info["url"]
    @url.setter
    def url(self, __value: Any) -> None:
        if not isinstance(__value, str) or not __value is None:
            raise TypeError("support to \'str\' not {type!r}".format(type=type(__value).__name__))
        if not endswith(__value, [".png", ".jpeg", ".jpg", ".webp", ".gif"]):
            raise TypeError("support to \'url links\' not {type!r}".format(type=type(__value).__name__))
        self._ep._info["url"] = __value
    def edit(self, **kwgs) -> None:
        self._ep._info["title"] = kwgs.get('title', self.title)
        self._ep._info["description"] = kwgs.get('description', self.description)
        self._ep._info["url"] = kwgs.get('url', self.url)
        self._ep.refresh()
def New_Family(
    Guild: Any,
    Name: str,
    role: Union[discord.Role, int],
    **kwargs: dict[str, Any]
) -> Family:
    FamilyNew["info"]["name"] = Name
    FamilyNew["info"]["id"] = role.id
    FamilyNew["info"]["habilitys"] = kwargs.get('habilitys', [])
    FamilyNew["info"]["rarity"] = kwargs.get('rarity', 0)
    FamilyNew["content"]["title"] = kwargs.get('title', None)
    FamilyNew["content"]["description"] = kwargs.get('description', None)
    FamilyNew["content"]["url"] = kwargs.get('url', None)
    FamilyNew["message"]["content"] = kwargs.get('content', None)
    FamilyNew["message"]["file"] = kwargs.get('url', None)
    Guild._familiys[Name] = FamilyNew
    Guild.save_all()
    return Family(
        Guild=Guild,
        Name=Name
    )