from typing import (Optional, Union, Any)
from .player import (Player, _PlayerHistoric)
from random import randint
from .npc import Npc
import discord
import json
import os
### -> Exceptions <- ###
from .errors import MissionNotFound, PlayerInMission

MissionNew = {"config": {"roles": ..., "count": None}, "content": {"IniEmbed": {"title": None, "description": None, "url": None}, "FinalEmbed": {"title": None, "description": None, "url": None}}, "reponseWebhookConfig": {"channels": ..., "npc": ..., "messages": []}}
_dir = './Json/Mission' if not __name__ == '__main__' else '../Json/Mission'
def embed(embed: dict[str, Any]) -> Optional[discord.Embed]:
    _embed = discord.Embed(title=embed['title'], description=embed['description'], colour=0x71368A)
    if not embed['url'] is None: _embed.set_image(url=embed['url'])
    return _embed
class _response:
    def __init__(self, response: dict[str, Any]) -> None:
        self.messages = response['messages']
        self.channels = response['channels']
        self.npc = Npc(response['npc'])
    async def send_messages(self, guild: discord.Guild) -> discord.TextChannel:
        channel = guild.get_channel(self.channels[randint(0, len(self.channels)-1)])
        webhook = await self.npc.get_webhook(channel=channel)
        for i in self.messages:
            if i['embed'] is None: await webhook.send(content=i['content'])
            else: await webhook.send(content='' if i['content'] is None else i['content'], embed=embed(i['embed']))
        await webhook.delete()
        return channel
class Mission:
    fmtDirectory: Optional[str]
    def __init__(self, Name: str, chr: Union[dict[str, Any], Union[str, bytes]]=_dir) -> None:
        if isinstance(chr, str) or isinstance(chr, bytes):
            self.fmtDirectory = str(os.path.join(str(chr if type(chr) is str else chr.decode()), Name)).replace('\\', '/')
            try:
                with open(os.path.join(self.fmtDirectory, "main.json"), 'r') as a:
                    chr = json.load(a)
            except FileNotFoundError: raise MissionNotFound(Name)
        self.chr = chr
        self.name = Name
        self.config: dict[str, Any] = self.chr["config"]
        self.content: dict[str, Any] = self.chr["content"]

        self._response: dict[str, Any] = self.chr["reponseWebhookConfig"]
        self._IniEmbed: dict[str, Any] = self.content["IniEmbed"]
        self._FinalEmbed: dict[str, Any] = self.content["FinalEmbed"]
        self._channel: Optional[discord.TextChannel] = None
    def __repr__(self) -> str: return self.name
    @property
    def response(self) -> _response: return _response(self._response)
    @property
    def IniEmbed(self) -> discord.Embed:
        _IniEmbed = self._IniEmbed
        _IniEmbed["title"] = str(self._IniEmbed["title"] if not self._IniEmbed["title"] is None else self.name)
        _IniEmbed["description"] = str(self._IniEmbed["description"].format(channel=str('' if self._channel is None else self._channel.mention)) if not self._IniEmbed["description"] is None else "No description")
        return embed(_IniEmbed)
    @property
    def FinalEmbed(self) -> discord.Embed:
        _FinalEmbed = self._FinalEmbed
        _FinalEmbed["title"] = str(self._FinalEmbed["title"] if not self._FinalEmbed["title"] is None else self.name)
        _FinalEmbed["description"] = str(self._FinalEmbed["description"] if not self._FinalEmbed["description"] is None else "No description")
        return embed(_FinalEmbed)
    @property
    def roles(self): return self.config["roles"]
    def Historic_Player(self, playerHistoric: _PlayerHistoric) -> None:
        playerHistoric.add_mission(self)
    async def start(self, player: Player) -> None:
        last = Player_Mission(player)
        if not last is None: raise PlayerInMission(user=player, mission1=self, mission2=last)
        self.response.npc.hearth = self.response.npc.IniHearth
        self.response.npc.stamina = self.response.npc.IniStamina
        self.Historic_Player(player.historic)
        self.response.npc.save_all()
    async def end(self, player: Player) -> None:
        player.historic.edit_last_mission()
def New_Mission(
    Name: str, 
    roles: list[Union[discord.Role, int]],
    npc: Npc,
    channels: list[Union[discord.TextChannel, int]],
    count: int=None,
    directory: Union[str, bytes]=_dir
    ) -> Mission:
    MissionNew["reponseWebhookConfig"]["channels"] = [i if type(i) is int else i.id for i in channels]
    MissionNew["config"]["roles"] = [i if type(i) is int else i.id for i in roles]
    MissionNew["reponseWebhookConfig"]["npc"] = str(npc)
    MissionNew["config"]["count"] = count
    try: os.mkdir(os.path.join(directory, Name))
    except: ...
    with open(os.path.join(directory, Name, "main.json"), 'w') as a:
        json.dump(MissionNew, a, indent=2)
    return Mission(Name=Name, chr=MissionNew)
def Serch_Mission(player: Player, directory: Union[str, bytes]=_dir) -> list[Mission]:
    missions = []
    for i in os.listdir(str(directory if isinstance(directory, str) else directory.decode('utf8'))):
        mission = Mission(i)
        for i in mission.roles:
            if i in player.roles:
                missions.append(mission)
    return missions
def Player_Mission(player: Player) -> Optional[Mission]:
    last = player.historic.get_last_mission()
    return None if last is None else Mission(last["name"])
if __name__ == '__main__': ...