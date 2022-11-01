from humanfriendly import parse_timespan
from discord.ext import commands
from discord import app_commands
from unidecode import unidecode
import requests
import discord
import utilz
### -> Exeptions <- ###
from utilz.errors import PlayerNotFound
from asyncio.exceptions import TimeoutError

def num_fmt(number: str):
    if number.lower().endswith("k"): return int(number[:-1]*1000)
    elif number.lower().endswith('m'): return int(number[:-1]*1000000)
    return int(number)

class Form(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name='new-form', description='Cria uma nova forma para uma respiração | kekkijutsu')
    async def NewForm(self, ints: discord.Interaction):
        await ints.response.send_modal(New_Form())
    @app_commands.command(name='add-new-box', description='Adiciona uma nova caixa para seu contexto')
    async def AddNewBox(self, ints: discord.Interaction, formname: str, content: str, roles: discord.Role=None):
        Resp, Form = utilz.Find_Form(directory=utilz.__Dirs__, Name=unidecode(str(formname)).lower())
        if not Resp is None:
            if Resp.clks == 'Respiration': str_fmt = '**Foi adicionado na Forma `{form}` da Respiração `{resp}` um novo contexto na posição `{position}`**'
            elif Resp.clks == 'Kekkijutsu': str_fmt = '**Foi adicionado na Forma `{form}` do kekkijutsu `{resp}` um novo contexto na posição `{position}`**'
            if not roles is None: tesr = Form.add_new_box(content=content, roles=[roles.id])
            else: tesr = Form.info.add_new_box(content=content, roles=[])
            await ints.response.send_message(str_fmt.format(form=Form.name.title(), resp=Resp.name.title(), position=tesr['position']))
        else: await ints.response.send_message('**Okok, caso queira criar essa forma de `!new-form {}`**, porquê não achei'.format(formname.lower()))
    @app_commands.command(name='edit-form')
    async def EditForm(self, ints: discord.Interaction, formname: str):
        Resp, Form = utilz.Find_Form(Name=unidecode(str(formname)).lower())
        if Resp is None: await ints.response.send_message('Procurei, procurei, e procurei. Mais não achei nenhuma forma com esse nome... Que pena'); return
        chrr = {}
        try: Player = utilz.Player(User=ints.user)
        except PlayerNotFound: Player = utilz.New_Player(User=ints.user)
        await ints.response.send_message(embed=utilz.embeds['edits']['editform'])
        msg = await ints.channel.send(embed=Form.set_embed(Player))
        while True:
            message: discord.Message = await self.bot.wait_for('message', timeout=300, check=lambda message: message.author.id == ints.user.id and message.channel.id == ints.channel.id); content = str(message.content); prefix = content.lower()
            if prefix.startswith('dis'):
                await message.reply('Todas as alterações foram descartadas'); return
            elif prefix.startswith('geral!'):
                chrr["description"] = content[6:]
                await message.delete()
            elif prefix.startswith('url!'):
                try: chrr["url"] = requests.get(url=content[4:]).url; await message.delete()
                except: await ints.channel.send('{user}, Opa eaí, tranquis? Então, não achei essa url, tem certeza que está certo?')
            elif prefix.startswith("dano!"):
                try: chrr["damege"] = num_fmt(content[5:]); await message.delete()
                except: await ints.channel.send('{user}, Opa eaí, tranquis? Então, não acho que esse número é válido, tem certeza que está certo?')
            elif prefix.startswith("stamina!"):
                try: chrr["stamina"] = num_fmt(content[8:]); await message.delete()
                except: await ints.channel.send('{user}, Opa eaí, tranquis? Então, não acho que esse número é válido, tem certeza que está certo?')
            elif prefix == 'done':
                Form.edit(**chrr)
                await message.reply('**Todas as alterações foram salvas**')
                return
            else:
                await message.delete()
            await msg.edit(embed=Form.set_embed(Player, **chrr))
    @app_commands.command(name='del-form', description='Apaga uma Forma')
    async def delform(self, ints: discord.Interaction, formname: str):
        Resp, Form = utilz.Find_Form(directory=utilz.__Dirs__, Name=unidecode(str(formname)).lower())
        if Resp is None: await ints.response.send_message(content='Tá, vamos lá, como eu apaguarei uma forma que nem existe?'); return
        Form.delete()
        await ints.response.send_message(content='Tudo certo chefe. Apaguei aqui')
    @app_commands.command(name='tesr-formembed')
    async def formembed(self, ints: discord.Interaction, resp: str, name: str):
        Resp = utilz.Respiration(resp)
        await ints.response.send_message(embed=Resp.forms.get(name).set_embed(utilz.Player(ints.user)))
    @app_commands.command(name="info-form")
    async def infoForm(self, ints: discord.Interaction, form: str):
        Resp, Form = utilz.Find_Form(form)
        await ints.response.send_message("`{0}`".format(Form.info))
def isNone(text: str):
    if text == '' or text.isspace(): return
    return text
def urlisNone(text: str):
    try: requests.get(url=text); return text
    except: return False
class New_Form(discord.ui.Modal, title='New Form'):
    text = '**Uma nova forma chamada `{form}` foi criada na respiração chamada `{resp}`**'
    RespName = discord.ui.TextInput(label='Nome da Respiração/Kekkijutsu', placeholder='Digite o nome da Respiração', required=True)
    FormName = discord.ui.TextInput(label='Nome da Forma', placeholder='Digite o nome da forma desejada', required=True)
    role = discord.ui.TextInput(label='Cargo da Forma', placeholder='[Opicional] - Digite o id do cargo da forma', required=False)
    description = discord.ui.TextInput(label='Descrição da Forma', style=discord.TextStyle.long, placeholder='[Opicional] - Digite a descrição da forma', required=False)
    async def on_submit(self, ints: discord.Interaction) -> None:
        Resp, Form = utilz.Find_Form(Name=unidecode(str(self.FormName)).lower())
        if not Resp is None: await ints.response.send_message('Essa forma já existe na respiração **`{resp}`**'.format(resp=str(Resp))); return
        Resp = utilz.Respirations(Name=unidecode(str(self.RespName)).lower())
        if Resp is None: await ints.response.send_message('A respiração ou kekkijutsu que lê me informou, não existe'); return
        Form = Resp.forms.new(Name=unidecode(str(self.FormName)).lower())
        await ints.response.send_message(str(self.text).format(form=str(Form), resp=str(Resp))); return
async def setup(bot: commands.Bot):
    await bot.add_cog(Form(bot), guilds=[discord.Object(id=971803172056219728)])