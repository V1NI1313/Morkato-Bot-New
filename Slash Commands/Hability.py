from discord.ext import commands
from discord import app_commands
from unidecode import unidecode
import requests
import discord
import utilz
### -> Exeptions <- ###
from utilz.errors import GuildNotExist, HabilityNotFound
### -> Functions and Abstractions <- ###
def inlineedecode(text: str, trac: list):
    if text.lower() in trac:
        return True
    return False
HabilityEditEmbed = discord.Embed(
    title='edit-hability',
    description='**╰⌲ ┊ Para editar uma habilidade, é só dar os comandos abaixo:\n\n\t╰⌲ ┊ title!\n\t┊ Troca o título da tal\n\n\t╰⌲ ┊ description!\n\t┊ Troca a descrição da habilidade\n\n\t╰⌲ ┊ url!\n\tTroca a imagem da habilidade**',
    colour=0x9B59B6
)
class Hability(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="hability")
    async def Hability(self, ints: discord.Interaction, hability: discord.Role) -> None: ...
    @app_commands.command(name='new-hability', description='Cria uma Habilidade')
    async def New_Hability(
        self,
        ints: discord.Interaction,
        name: str,
        role: discord.Role,
        title: str=None,
        description: str=None,
        url: str=None
    ) -> None:
        try: Guild = utilz.Guild(ints.guild)
        except GuildNotExist: Guild = utilz.New_Guild(ints.guild)
        try:
            Habi = Guild.habilitys.get(role)
            await ints.response.send_message("**Uma habilidade chamada `{name}`, já existe!**".format(name=Habi.name)); return
        except HabilityNotFound: ...
        kwgs = {}
        MESSAGE_ALERT = False
        if not title is None: kwgs["title"] = title
        if not description is None: kwgs["description"] = description
        if not url is None:
            try: kwgs["url"] = str(requests.get(url=url).url)
            except: MESSAGE_ALERT = True
        Habi = Guild.habilitys.new(
            Name=unidecode(name).lower().replace(' ', '-'),
            role=role,
            **kwgs
        )
        await ints.response.send_message("**Uma nova habilidade chamada `{name}` foi criada!**".format(name=Habi.name))
        if MESSAGE_ALERT: await ints.channel.send("**{user} o parâmetro `url` que me passou, Então... Eu não achei a tal imagem, será que está certo?**".format(user=ints.user.mention))
    @app_commands.command(name='tesr-player')
    async def ___(self, ints: discord.Interaction, family: discord.Role):
        Guild = utilz.Guild(ints.guild)
        # Player = Guild.players.get(ints.user)
        # await ints.response.send_message("**Player `{player}` habilitys `{habis}`**".format(player=str(Player), habis=str(Player.habilitys)))
        # habi = Guild.habilitys.random(Player, 3)
        # await Player.User.add_roles(*tuple([i.role for i in habi]))
        # await ints.response.send_message("**Player `{player}` habilitys `{habis}`**".format(player=str(Player), habis=str(["{name} - {rarety}".format(name=i.name, rarety=utilz.FormatRarety(i.rarity)) for i in habi])))
        Family = Guild.familys.get(family)
        await ints.response.send_message(str(Guild.players.getfromFamily(Family)))
    @app_commands.command(name='edit-hability')
    async def Edit_Hability(
        self,
        ints: discord.Interaction,
        hability: discord.Role,
        title: str=None,
        description: str=None
    ):
        try: Guild = utilz.Guild(ints.guild)
        except GuildNotExist: Guild = utilz.New_Guild(ints.guild)
        try: Hability = Guild.habilitys.get(hability)
        except HabilityNotFound: await ints.response.send_message("**Opa, eu acho que essa habilidade não existe... Pelo menos eu não achei .-.**")
        kwgs = {}
        await ints.response.send_message(embed=HabilityEditEmbed)
        DELETE_MESSAGE = False
        if not title is None: kwgs["title"] = title
        if not description is None: kwgs["description"] = description
        while True:
            try:
                message: discord.Message = await self.bot.wait_for(
                "message",
                timeout=120,
                check=lambda message: message.channel.id == ints.channel.id and message.author.id == ints.user.id
            )
                if '!' in message.content:
                    content, prefix = message.content[message.content.find('!')+1:], message.content[:message.content.find('!')].lower()
                else: content, prefix = message.content, None
                
                image = bool(len(message.attachments))
            except TimeoutError:
                await ints.edit_original_response(content="Opa {user}, você demorou muito para me resoponder, até mais!", embeds=[]); return
            if prefix == 'title':
                kwgs["title"] = content
                DELETE_MESSAGE = True
            elif prefix == 'description':
                kwgs["description"] = content
                DELETE_MESSAGE = True
            elif prefix == 'url':
                _url = get_url(message, image, content)
                try: kwgs["url"], DELETE_MESSAGE = requests.get(url=_url).url, True
                except: await message.add_reaction('❌')
            elif content == 'done' and prefix is None:
                if len(kwgs) == 0: await message.reply("**Bem... Eu acho que salvei. É que você não editou nada tlgd**"); return
                await _message.add_reaction('✅')
                await _message.add_reaction('❌')
                try: reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    timeout=120,
                    check=lambda reaction, user: reaction.message.channel.id == _message.channel.id and user.id == ints.user.id
                )
                except TimeoutError: await _message.clear_reactions(); return
                if str(reaction.emoji) == '✅':
                    Hability.edit(**kwgs)
                    await message.reply("**Tudo certo chefe! salvei aqui.**")
                elif str(reaction.emoji) == '❌':
                    await message.reply("**Éh, que pena que não gostou**")
                await _message.clear_reactions()
                return
            elif content == 'dis' and prefix is None:
                await message.reply("**Todas as informações foram descartadas!**"); return
            _message = await ints.edit_original_response(embeds=[Hability.embed(**kwgs)])
            if DELETE_MESSAGE:
                await message.delete()
                DELETE_MESSAGE = False
    @app_commands.command(name="send-hability")
    async def Send_Hability(self, ints: discord.Interaction, hability: discord.Role, channel: discord.TextChannel=None) -> None:
        Guild = utilz.Guild(ints.guild)
        Hability = Guild.habilitys.get(hability)
        _channel = ints.channel if channel is None else channel
        webhook = await _channel.webhooks()
        await webhook[0].send(embed=Hability.embed())
    @app_commands.command(name="all-hability")
    async def all_hability(self, ints: discord.Interaction) -> None:
        try: Guild = utilz.Guild(ints.guild)
        except GuildNotExist: Guild = utilz.New_Guild(ints.guild)
        for i in Guild.habilitys.values():
            try: text = "{_text}{text}\n".format(_text=text, text=str(i.role.mention))
            except: text = "{role}\n".format(role=str(i.role.mention))
        try: await ints.response.send_message(text)
        except: await ints.channel.send(text)
    @app_commands.command(name="hability-add-role")
    async def Hability_add_role(
        self,
        ints: discord.Interaction,
        hability: discord.Role,
        require: str,
        role1: discord.Role,
        role2: discord.Role=None,
        role3: discord.Role=None,
        role4: discord.Role=None,
        role5: discord.Role=None,
        role6: discord.Role=None,
        role7: discord.Role=None,
        role8: discord.Role=None,
        role9: discord.Role=None,
        role10: discord.Role=None,
        role11: discord.Role=None,
        role12: discord.Role=None
    ) -> None:
        try: Guild = utilz.Guild(ints.guild)
        except GuildNotExist: Guild = utilz.New_Guild(ints.guild)
        try: _hability = Guild.habilitys.get(hability)
        except HabilityNotFound: await ints.response.send_message("**Opa amigão, então... Essa habilidade não existe '-'**"); return
        roles = [role1]
        if not role2 is None: roles.append(role2)
        if not role3 is None: roles.append(role3)
        if not role4 is None: roles.append(role4)
        if not role5 is None: roles.append(role5)
        if not role6 is None: roles.append(role6)
        if not role7 is None: roles.append(role7)
        if not role8 is None: roles.append(role8)
        if not role9 is None: roles.append(role9)
        if not role10 is None: roles.append(role10)
        if not role11 is None: roles.append(role11)
        if not role12 is None: roles.append(role12)
        _hability.add_role(int(require), *tuple(roles))
        text = "".join(["**`{i}` - Um novo cargo {role} foi adicionado para a habilidade `{habi}`!**\n".format(i=i+1, role=role.mention, habi=_hability.name) for i, role in enumerate(roles)])
        try: await ints.response.send_message(text)
        except: await ints.channel.send(text)
async def setup(bot: commands.Bot): await bot.add_cog(Hability(bot), guilds=[discord.Object(id=971803172056219728), discord.Object(id=1030300817175089203)])
def end(text: str, ends: list[str]): return True in [text.endswith(i) for i in ends]
def get_url(message: discord.Message, image: bool, content: str) -> str:
    if image and end(message.attachments[0].url, [".png", ".jpeg", ".jpg", ".webp", ".gif"]):
        return message.attachments[0].url
    return content