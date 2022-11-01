from discord.ext import commands
from discord import app_commands
from unidecode import unidecode
from typing import (Optional, Union)
import requests
import discord
import utilz
### -> Exceptions <- ###
from utilz.errors import PlayerNotFound, HabilityNotFound, NpcNotFound
### -> Functions and Abstractions <- ###
def formatText(text: str) -> str:
    if text.isspace() or text == '': return
    numInitial = 0
    numFinal = len(text)-1
    while text[numInitial] == ' ': numInitial += 1
    while text[numFinal] == ' ': numFinal -= 1
    return text[numInitial:numFinal+1]
def fillterHability(hability: str) -> list:
    allHabi = []
    errors = []
    for i in hability.split(';'):
        i = formatText(i)
        if not i is None:
            try: allHabi.append(utilz.Hability(Name=i.lower().replace(' ', '-')))
            except HabilityNotFound: errors.append('**A habilidade chamada `{habi}` não existe, e por isso não dará buffs... Uai, não existe msm.**'.format(habi=i))
    return errors, allHabi
async def responseNpc(ints: discord.Interaction, player: utilz.Player, Form: utilz.respiration.Form, npc: Optional[str]) -> None:
    if npc is None:
        await ints.response.send_message(embed=Form.set_embed(player)); return
    npc: utilz.Npc = utilz.Npc(Name=formatText(npc))
    if npc.hearth == -1:
        await ints.response.send_message('**Como você quer atacar um npc morto?**'); return
    npc.hearth -= Form.damege
    await ints.response.send_message(embed=Form.set_embed(player))
    mission = utilz.Player_Mission(player)
    if not mission is None and mission.response.npc.Name == npc.Name and npc.hearth == -1:        
        await ints.channel.send(embed=mission.FinalEmbed)
        await mission.end(player)
    else:
        webhook = await npc.get_webhook(ints.channel)
        await webhook.send('> **`{user}` Me atacou, meu status agora é: **\n> **•「❤️」{_damege}**\n> **•「💨」{_stamina}**\n> **Por que `{user}`, por quê você me atacou?**'.format(_damege=utilz.num_fmt(npc.hearth), _stamina=utilz.num_fmt(npc.stamina), user=str(ints.user)))
        await webhook.delete()
    npc.save_all()
class PVP(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name='a', description='Ataca usando uma forma junto há uma habilidade')
    async def Attack(self, ints: discord.Interaction, form_name: str, hability: str=None, npc: str=None):
        Resp, Form = utilz.Find_Form(Name=unidecode(str(form_name)).lower())
        if Resp is None: await ints.response.send_message('Procurei, procurei e, procurei. Mais não achei nada'); return
        try: Player = utilz.Player(User=ints.user)
        except PlayerNotFound: Player = utilz.New_Player(User=ints.user)
        textErrors = ''
        textHabis = ''
        if not hability is None:
            errors, allHabi = fillterHability(hability)
            errorsForm, habis = Form.set_status(Player, allHabi)
            textErrors = '{errors}{errorsF}'.format(errors='' if len(errors) == 0 else '> **Erros tipo - `utilz.errors.HabilityNotFound`**:\n> {0}\n'.format("\n> ".join(errors)), errorsF='' if len(errorsForm) == 0 else '> **Erros tipo - `utilz.Hability.role.PlayerNotPermission`***\n> {0}'.format("\n> ".join(errorsForm)))
            textHabis = '\n'.join(['> **`{user}` usou `{_habi}`**'.format(user=str(ints.user), _habi=i.name) for i in habis])
        await responseNpc(ints, Player, Form, npc)
        if not textHabis == '': await ints.channel.send(textHabis)
        if not textErrors == '': await ints.channel.send('> {user} Apenas olhe:\n\n{text}'.format(user=str(ints.user.mention), text=textErrors))
    @app_commands.command(name='separtor')
    async def separator(self, ints: discord.Interaction, text: str) -> None:
        await ints.response.send_message('`{}`'.format('; '.join([str(formatText(i)) for i in text.split(';')])))
async def setup(bot: commands.Bot): await bot.add_cog(PVP(bot), guilds=[discord.Object(id=971803172056219728)])