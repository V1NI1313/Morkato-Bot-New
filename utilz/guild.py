from .hability import Hability, New_Hability
from typing import (Optional, Union, Any)
from .family import Family, New_Family
from .player import Player, New_Player
from .functions import FormatRarety
import discord
import random
import json
import os
### -> Exeptions <- ###
from .errors import (
    GuildAlredyExists,
    GuildNotExist,
    HabilityNotFound,
    PlayerNotFound,
    FamilyNotFound
)

_dir = "./Json/Guilds"

class _GuildRespirations(dict): ...
class _GuildKekkijutsus(_GuildRespirations): ...
class _GuildNpcs(dict): ...
class Guild:
    def __init__(
        self,
        Guild: discord.Guild,
        chr: Union[str, bytes]=_dir
    ) -> None:
        self.disGuild = Guild

        self.fmtDirectory: Optional[str] = os.path.join(str(chr if isinstance(chr, str) else chr.decode('utf8')), str(Guild.id))
        self.directory = chr
        try:
            with open(os.path.join(self.fmtDirectory, "players.json"), 'r') as a: self._players: dict[str, Any] = json.load(a)
            with open(os.path.join(self.fmtDirectory, "habilitys.json"), 'r') as a: self._habilitys: dict[str, Any] = json.load(a)
            with open(os.path.join(self.fmtDirectory, "kekkijutsus.json"), 'r') as a: self._kekkijutsus: dict[str, Any] = json.load(a)
            with open(os.path.join(self.fmtDirectory, "respirations.json"), 'r') as a: self._respirations: dict[str, Any] = json.load(a)
            with open(os.path.join(self.fmtDirectory, "familiys.json"), 'r') as a: self._familys: dict[str, Any] = json.load(a)
            with open(os.path.join(self.fmtDirectory, "npcs.json"), 'r') as a: self._npcs: dict[str, Any] = json.load(a)
        except: raise GuildNotExist(Guild)

        self.habilitys: _GuildHabilitys[str, Hability] = _GuildHabilitys(self)
        self.familys: _GuildFamilys[str, Family] = _GuildFamilys(self)
        self.players: _GuildPlayers[str, Player] = _GuildPlayers(self)
    def __repr__(self) -> str: return str(self.disGuild)
    def __eq__(self, __key: Any) -> bool:
        if not isinstance(__key, Guild):
            raise TypeError("Support to `utilz.Guild` not `{type}`".format(type=type(__key).__name__))
        return __key.disGuild.id == self.disGuild.id
    def save_all(self) -> None:
        with open(os.path.join(self.fmtDirectory, "players.json"), 'w') as a: json.dump(self._players, a, indent=2)
        with open(os.path.join(self.fmtDirectory, "habilitys.json"), 'w') as a: json.dump(self._habilitys, a, indent=2)
        with open(os.path.join(self.fmtDirectory, "kekkijutsus.json"), 'w') as a: json.dump(self._kekkijutsus, a, indent=2)
        with open(os.path.join(self.fmtDirectory, "respirations.json"), 'w') as a: json.dump(self._respirations, a, indent=2)
        with open(os.path.join(self.fmtDirectory, "familiys.json"), 'w') as a: json.dump(self._familys, a, indent=2)
        with open(os.path.join(self.fmtDirectory, "npcs.json"), 'w') as a: json.dump(self._npcs, a, indent=2)
        self.__init__(self.disGuild, self.directory)
class _GuildPlayers(dict):
    def __init__(self, guild: Guild) -> None:
        self.__iniGuild = guild
        players = {}
        for i in guild._players:
            players[i] = Player(self.__iniGuild, i)
        super().__init__(players)
    def get(self, arg: Union[discord.Member, str, int]) -> Player:
        for i in self.values():
            if ((
              isinstance(arg, discord.Member)
              or isinstance(arg, int)
            ) and int(arg if isinstance(arg, int) else arg.id) == i.User.id): return i
            elif str(arg) == str(i.User): return i
        raise PlayerNotFound(str(arg))
    def new(self, Member: discord.Member, nick: str, **kwargs) -> Player:
        player = New_Player(
            self.__iniGuild,
            Member,
            Name=nick,
            **kwargs
        )
        self[str(Member.id)] = player
        return player
    def getfromFamily(self, family: Family) -> list[Player]:
        players = []
        for i in self.values():
            if not i.family is None and i.family == family:
                players.append(i)
        return (
            players
            if len(players)
            else None
        )
class _GuildHabilitys(dict):
    def __init__(self, guild: Guild) -> None:
        self.__iniGuild = guild
        habilitys = {}
        for i in guild._habilitys:
            habilitys[i] = Hability(self.__iniGuild, i)
        super().__init__(habilitys)
    def get(self, arg: Union[discord.Role, str, int]) -> Hability:
        for i in self.values():
            if ((
                isinstance(arg, discord.Role) or isinstance(arg, int)
            ) and i.role.id == int(arg if isinstance(arg, int) else arg.id)): return i
            elif isinstance(arg, str) and i.name == arg: return i
        raise HabilityNotFound(str(arg))
    def getforPlayer(self, player: Player) -> Optional[list[Hability]]:
        habilitys = []
        for i in self.values():
            if i.role in player.User.roles: habilitys.append(i)
        return (
            habilitys
            if len(habilitys)
            else None
        )
    def getrequireforPlayer(self, player: Player) -> Optional[list[Hability]]:
        habilitys = []
        for i in self.values():
            if i.VerificationRequirePlayer(player):
                habilitys.append(i)
        return (
            habilitys
            if len(habilitys)
            else None
        )
    def _filter(self, habilitys: list[Hability]) -> dict[int, list[Hability]]:
        _chr = {}
        for i in habilitys:
            try: _chr[i.rarity].append(i)
            except: _chr[i.rarity] = [i]
        return _chr
    def filter(self, player: Player) -> Optional[dict[str, list[Hability]]]:
        habilitys = self.getrequireforPlayer(player)
        if habilitys is None: return
        habilitys = self._filter(habilitys)
        habilitys = list(habilitys.items())
        for i, _i in enumerate(habilitys):
            habilitys[i] = (FormatRarety(_i[0]), habilitys[i][1])
        return dict(habilitys)
    def random(self, player: Player, index: int = 1) -> list[Hability]:
        habilitys = self.getrequireforPlayer(player)
        if len(habilitys) == 0: return
        if not player.habilitys is None:
            for i in player.habilitys:
                if i in habilitys: del habilitys[habilitys.index(i)]
        if index > len(habilitys):
            index = len(habilitys)
        habilitys = self._filter(habilitys)
        _habilitys = []
        for i in range(index):
            number = random.random()
            LOOP = True
            while LOOP:
                if number >= 0.4:
                    if not 0 in habilitys:
                        number = 0.1
                        continue
                    _len = len(habilitys[0])-1
                    _index = random.randint(0, int(_len if not _len == -1 else 0))
                    _habilitys.append(habilitys[0][_index])
                    del habilitys[0][_index]
                    LOOP = False
                elif number >= 0.1 and number < 0.4:
                    if not 1 in habilitys: 
                        number = 0.05
                        continue
                    _len = len(habilitys[1])-1
                    _index = random.randint(0, int(_len if not _len == -1 else 0))
                    _habilitys.append(habilitys[1][_index])
                    del habilitys[1][_index]
                    LOOP = False
                elif number >= 0.05 and number < 0.1:
                    if not 2 in habilitys:
                        number = 0.4
                        continue
                    _len = len(habilitys[2])-1
                    _index = random.randint(0, int(_len if not _len == -1 else 0))
                    _habilitys.append(habilitys[2][_index])
                    del habilitys[2][_index]
                    LOOP = False
                elif number < 0.05:
                    if not 3 in habilitys:
                        number = 0.4
                        continue
                    _len = len(habilitys[3])-1
                    _index = random.randint(0, int(_len if not _len == -1 else 0))
                    _habilitys.append(habilitys[3][_index])
                    del habilitys[3][_index]
                    LOOP = False
        return _habilitys
        
    def new(self, Name: str, role: Union[discord.Role, int], **kwargs) -> Hability:
        hability = New_Hability(
            self.__iniGuild,
            Name,
            role,
            **kwargs
        )
        self[Name] = hability
        return hability
class _GuildFamilys(dict):
    def __init__(self, Guild: Guild) -> None:
        self._ep = Guild
        familys = {}
        for i in self._ep._familys:
            familys[i] = Family(Guild, i)
        super().__init__(familys)
    def get(self, arg: Union[discord.Role, str, int]) -> Family:
        for i in self.values():
            if ((
                isinstance(arg, discord.Role) or isinstance(arg, int)
            ) and i.role.id == int(arg if isinstance(arg, int) else arg.id)): return i
            elif isinstance(arg, str) and i.name == str(arg): return i
        raise FamilyNotFound(arg)
    def getforPlayer(self, player: Player) -> Optional[Family]:
        for i in self.values():
            if i.role in player.User.roles: return i
        return None
    def getrequireforPlayer(self, player: Player) -> list[Family]:
        familys = []
        for i in self.values():
            if i.VerificationRequirePlayer(player):
                familys.append(i)
        return (
            familys
            if len(familys)
            else None
        )
    def new(
        self,
        Name: str,
        role: Union[discord.Role, int],
        **kwargs
    ) -> Family:
        family = New_Family(
            self._ep,
            Name=Name,
            role=role,
            **kwargs
        )
        self[Name] = family
        return family
GuildNew = {"players": {}, "respirations": {}, "kekkijutsus": {}, "habilitys": {}, "npcs": {}, "familiys": {}}
def New_Guild(guild: discord.Guild, directory: str=_dir) -> Guild:
    fmtDirectory = str(os.path.join(directory, str(guild.id)))
    try: os.mkdir(fmtDirectory)
    except: raise GuildAlredyExists(guild)
    for i in GuildNew:
        with open(os.path.join(fmtDirectory, "{file}.json".format(file=i)), 'w') as a:
            json.dump(GuildNew[i], a)
    return Guild(guild, directory)