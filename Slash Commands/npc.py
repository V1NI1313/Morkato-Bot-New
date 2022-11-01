from discord.ext import commands
from discord import app_commands
from unidecode import unidecode
import requests
import discord
import utilz
### -> Exceptions <- ###
from utilz.errors import NpcNotFound

class Npc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name='new-npc', description='Cria um novo npc')
    async def New_Npc(self, ints: discord.Interaction, npc_name: str, user: discord.User=None):
        try:
            npc = utilz.Npc(Name=unidecode(str(npc_name)).lower())
            await ints.response.send_message('**Esse npc já existe!**')
        except NpcNotFound: npc = utilz.New_Npc(Name=unidecode(str(npc_name)).lower(), player=utilz.Player(ints.user))
        await ints.response.send_message(str(npc))
    @app_commands.command(name='tesr-npc')
    async def tesr_npc(self, ints: discord.Interaction, npc_name: str, content: str):
        npc = utilz.Npc(Name=unidecode(str(npc_name)).lower())
        url = npc.info.url
        if not url is None:
            url = requests.get(url).content
        webhook = await ints.channel.create_webhook(name='{name} | ❤️ {life} | 💨 {stamina}'.format(name=str(npc), life=str(utilz.num_fmt(npc.hearth)), stamina=str(utilz.num_fmt(npc.stamina))), avatar=url)
        await webhook.send(content)
        await webhook.delete()
        await ints.response.send_message('Success Response, conected webhook', ephemeral=True)
    @app_commands.command(name='npc-attack')
    async def npc_attack(self, ints: discord.Interaction, npc_name: str, form_name: str):
        Resp, Form = utilz.Find_Form(Name=unidecode(str(form_name)).lower())
        if Resp is None: await ints.response.send_message('**Essa forma não existe!**'); return
        try: npc = utilz.Npc(Name=unidecode(str(npc_name)).lower())
        except NpcNotFound: await ints.response.send_message('**Esse npc não existe!**')
        url = npc.info.url
        if not url is None:
            url = requests.get(url).content
        webhook = await ints.channel.create_webhook(name='{name} | ❤️ {life} | 💨 {stamina}'.format(name=str(npc), life=str(utilz.num_fmt(npc.hearth)), stamina=str(utilz.num_fmt(npc.stamina))), avatar=url)
        await ints.response.send_message('Opa {user} rolou um erro tipo **`discord.errors.HTTPException`** desculpe-me pelo erro, espero resolvê-lo logo '.format(user=str(ints.user)))
        msg = await webhook.send(embed=Form.set_embed(npc))
        await webhook.delete()
        await ints.response.send_message('> **Npc damege:**\n> **•「❤️」{damege}**\n> **•「💨」{stamina}**'.format(damege=str(utilz.num_fmt(Form.damege)), stamina=str(utilz.num_fmt(Form.stamina))))
    @app_commands.command(name='role-npc')
    async def role_npc(self, ints: discord.Interaction, npc_name: str):
        try: npc = utilz.Npc(Name=unidecode(str(npc_name)).lower())
        except NpcNotFound: await ints.response.send_message('**Esse npc não existe!**'); return
        url = npc.info.url
        if not url is None:
            url = requests.get(url).content
        webhook = await ints.channel.create_webhook(name='{name}'.format(name=str(npc)), avatar=url)
        roles = ['{i} - {name}'.format(i=str(i+1), name=str(ints.guild.get_role(chr).name)) for i, chr in enumerate(npc.roles)]
        await webhook.send('Opa {user}, meus cargos estão logo aí.\n`{roles}`'.format(user=str(ints.user.mention), roles='No role' if roles == [] else '\n'.join(roles)))
        await webhook.delete()
        await ints.response.send_message('Success Response, conected webhook', ephemeral=True)
    @app_commands.command(name='npc-card')
    async def npc_card(self, ints: discord.Interaction, npc_name: str) -> None:
        try: npc = utilz.Npc(Name=unidecode(str(npc_name)).lower())
        except NpcNotFound: await ints.response.send_message('**Esse npc não existe!**'); return
        await ints.response.send_message(embed=npc.info.card(ints.guild))
async def setup(bot: commands.Bot):
    await bot.add_cog(Npc(bot), guilds=[discord.Object(id=971803172056219728)])