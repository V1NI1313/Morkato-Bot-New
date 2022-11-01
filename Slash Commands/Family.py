from io import BytesIO
from sys import prefix
from discord import app_commands
from discord.ext import commands
from unidecode import unidecode
import requests
import discord
import utilz
### -> Exceptions <- ###
from utilz.errors import GuildNotExist, FamilyNotFound

FamilyEditEmbed: discord.Embed = discord.Embed(
    title="Edit-family",
    description="**╰⌲ ┊ Para editar uma família... Nossa é até estranho falar isso, mais... Enfim. Você terá que dar os comandos abaixo :p\n\n\t╰⌲ ┊ title!\n\t┊ Edita o título da embed\n\n\t╰⌲ ┊ description!\n\t┊ Edita a descrição da embed\n\n\t╰⌲ ┊ url!\n\t┊ Edita a imagem url da embed\n\t┊ Sujeito à erro\n\n\t╰⌲ ┊ message!\n\t┊ Troca o conteúdo da mensagem\n\n\t╰⌲ ┊ file!\n\t┊ Troca o binário da mensagem**",
    colour=0x9B59B6
)

class Family(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    @app_commands.command(name="new-family", description="Cria uma nova família")
    async def New_Family(
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
            family = Guild.familys.get(role)
            await ints.response.send_message("**Opa, amigão. Então, essa família já existe, tente uma outra :D**"); return
        except FamilyNotFound: ...
        kwgs = {}
        MESSAGE_ALERT = False
        if not title is None: kwgs["title"] = title
        if not description is None: kwgs["description"] = description
        if not url is None:
            try: kwgs["url"] = requests.get(url=url).url
            except: MESSAGE_ALERT = True
        family = Guild.familys.new(
            Name=unidecode(name).lower().replace(' ', '-'),
            role=role,
            **kwgs
        )
        await ints.response.send_message("**Uma nova família chamada `{family}` foi criada!**".format(family=str(family.name)))
        if MESSAGE_ALERT: await ints.channel.send("**{user} o parâmetro `url` que me passou, Então... Eu não achei a tal imagem, será que está certo?**".format(user=ints.user.mention))
    @app_commands.command(name="family-add-hability")
    async def Family_add_role(
        self,
        ints: discord.Interaction,
        family: discord.Role,
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
        try: _family = Guild.familys.get(family)
        except FamilyNotFound: await ints.response.send_message("**Opa, amigão. Então, essa família já existe, tente uma outra :D**"); return
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
        Habilitys = _family.habilitys.add(*tuple(roles))
        await ints.response.send_message("**Sucesso: `{habilitys}`\nErro: `{err}`**".format(habilitys=len(Habilitys), err=str(len(roles)-len(Habilitys))))
    @app_commands.command(name="edit-family", description="Edita uma família")
    async def Edit_Family(
        self,
        ints: discord.Interaction,
        family: discord.Role,
        title: str=None,
        description: str=None,
        url: str=None,
        message_content: str=None,
        file_url: str=None
    ) -> None:
        try: Guild = utilz.Guild(ints.guild)
        except GuildNotExist: Guild = utilz.New_Guild(ints.guild)
        try: _family = Guild.familys.get(family)
        except FamilyNotFound: await ints.response.send_message("**Opa, amigão. Então, essa família já existe, tente uma outra :D**"); return
        kwgs = {}
        MESSAGE_ALERT = False
        DELETE_MESSAGE = False
        if not title is None: kwgs['title'] = title
        if not description is None: kwgs["description"] = description
        if not url is None:
            try: kwgs["url"] = requests.get(url=url).url
            except: MESSAGE_ALERT = True
        await ints.response.send_message(embed=FamilyEditEmbed)        
        while True:
            try:
                message: discord.Message = await self.bot.wait_for(
                    'message',
                    timeout=180,
                    check=lambda message: (
                        message.author.id == ints.user.id
                        and message.guild.id == ints.guild.id 
                        and message.channel.id == ints.channel.id
                    )
                )
                index = message.content[:21].find('!')
                print(index)
                if not index == -1: prefix, content = message.content[:index].lower(), message.content[index+1:]
                else: content, prefix = message.content, None
            except TimeoutError: await ints.edit_original_response(content="Você demorou demais, Bye!"); return
            if prefix == 'title':
                kwgs["title"] = content
                DELETE_MESSAGE = True
            elif prefix == 'description':
                kwgs["description"] = content
                DELETE_MESSAGE = True
            elif prefix == 'url':
                try: kwgs["url"], DELETE_MESSAGE, MESSAGE_ALERT = requests.get(url=content).url, True, False
                except: message.add_reaction('❌')
            elif prefix == 'message':
                kwgs["content"] = content
                DELETE_MESSAGE = True
            elif prefix == 'file':
                try: kwgs["file"], DELETE_MESSAGE = requests.get(url=content).url, True
                except: message.add_reaction('❌')
            elif content == 'done' and prefix is None:
                _family.edit(**kwgs)
                await message.reply("**Tudo certo chefe! Salvei aqui :D**")
                if MESSAGE_ALERT: await ints.channel.send("**Opa chefe, então... Em um dos parâmetros deu algum erro. Eu acho que foi no `url`**")
                return
            if DELETE_MESSAGE:
                await message.delete()
                DELETE_MESSAGE = False
            await ints.edit_original_response(embed=_family.embed(**kwgs))
    @app_commands.command(name="family-send-message")
    async def send_message(self, ints: discord.Interaction, family: discord.Role) -> None:
        try: Guild = utilz.Guild(ints.guild)
        except GuildNotExist: Guild = utilz.New_Guild(ints.guild)
        try: _family = Guild.familys.get(family)
        except FamilyNotFound: await ints.response.send_message("**Opa, amigão. Então, essa família já existe, tente uma outra :D**"); return
        kwgs = {"content": _family.content}
        if not _family.file is None:
            with BytesIO() as a:
                a.write(requests.get(_family.file).content)
                a.seek(0)
                await ints.channel.send(_family.content, file=discord.File(a, f"family.gif"))
            return
        await ints.response.send_message(**kwgs)
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Family(bot), guild=discord.Object(id=1030300817175089203))