import json
from discord.ext import commands
from discord import app_commands
from unidecode import unidecode
from random import randint
import discord
import utilz
import re
### -> Exptions <- ###
from utilz.errors import (MissionNotFound, PlayerNotFound, PlayerInMission, NpcNotFound)

class Mission(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    @app_commands.command(name='new-mission', description='Cria uma nova missão')
    async def New_Mission(
        self, 
        ints: discord.Interaction, 
        name: str,
        npc: str,
        role: discord.Role,
        channel: discord.TextChannel,
        count: int=None,
    ) -> None:
        try: Npc = utilz.Npc(Name=unidecode(str(npc)).lower().replace(' ', '-'))
        except NpcNotFound: await ints.response.send_message('**O npc chamado `{npc}` não existe**'.format(npc)); return
        try: utilz.Mission(Name=unidecode(str(name)).lower().replace(' ', '-')); await ints.response.send_message('**A tal missão já existe**'); return
        except MissionNotFound: mission = utilz.New_Mission(
            Name=unidecode(str(name)).lower().replace(' ', '-'),
            npc=Npc,
            channels=[channel],
            roles=[role],
            count=count
        )
        await ints.response.send_message('**Uma nova missão chamada `{mission}` foi criada**'.format(mission=str(mission)))

    @app_commands.command(name='mission', description='Da uma missão ao usuário')
    async def Mission(self, ints: discord.Interaction) -> None:
        try: Player = utilz.Player(User=ints.user)
        except PlayerNotFound: Player = utilz.New_Player(User=ints.user)
        missions = utilz.Serch_Mission(Player)
        if len(missions) == 0:
            await ints.response.send_message('**Procurei aqui, e parece que você não tem nenhuma missão para fazer.**')
        mission = missions[randint(0, len(missions))-1]
        try: await mission.start(Player)
        except PlayerInMission as a: await ints.response.send_message('**Você já está em uma missão chamada `{name}`, como que fara a tal missão ao tempo 🤔**'.format(name=str(a.InMission.name))); return
        mission._channel = await mission.response.send_messages(guild=ints.guild)
        await ints.response.send_message(embed=mission.IniEmbed)
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Mission(bot), guilds=[discord.Object(id=971803172056219728)]) 