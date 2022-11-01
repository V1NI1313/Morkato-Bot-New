from discord.ext import commands
from discord import app_commands
from unidecode import unidecode
import requests
import discord
import utilz
### -> Exeptions <- ###
from utilz.errors import RespirationNotFound

class Respiration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name='respiration', description='Exibe informações da respiração')
    async def Respiration(self, ints: discord.Interaction, name: str=None):
        if name is None: await ints.response.send_message(embed=RespsFmt(utilz._dirs[0])); return
        try: Resp = utilz.Respiration(Name=unidecode(str(name)).lower().replace(' ', '-'))
        except RespirationNotFound: await ints.response.send_message('Procurei, procurei. E não achei.'); return
        embeds = Resp.embeds
        if len(embeds) == 1: await ints.response.send_message(embed=embeds[0]); return
        await ints.response.send_message(embed=embeds[0], view=myButtom(embeds, ints))
    @app_commands.command(name='new-respiration', description='Cria uma respiração, claro se não tiver uma já existente')
    async def New_Respiration(self, ints: discord.Interaction, name: str, role: discord.Role=None):
        verification = utilz.Respirations(Name=unidecode(str(name)).lower().replace(' ', '-'))
        if not verification is None:
            text = str('**Essa respiração já existe**' if verification.type == 'Respiration' else '**Essa respiração não existe, mais existe um kekkijutsu com esse nome**')
            await ints.response.send_message(text); return
        Resp = utilz.New_Respiration(
            Name=unidecode(str(name)).lower().replace(' ', '-'),
            role=role if role is None else role.id
        )
        await ints.response.send_message('**Foi criado uma nova respiração chamada `{resp}`** :D'.format(resp=str(Resp)))
    @app_commands.command(name='edit-resp', description='Edita uma respiração')
    async def Edit_Resp(self, ints: discord.Interaction, respname: str):
        try: Resp = utilz.Respiration(Name=unidecode(str(respname)).lower().replace(' ', '-'))
        except RespirationNotFound: await ints.response.send_message('**Cansei de procurar essa respiração, sério, nunca acho. Agora, procura você.**')
        await ints.response.send_message(embed=utilz.embeds['edits']['editresp'])
        edit, chr = {}, []
        while True:
            try: message: discord.Message = await self.bot.wait_for('message', timeout=300, check=lambda message: message.channel.id == ints.channel.id and message.author.id == ints.user.id); prefix = str(message.content).lower(); content = str(message.content)
            except TimeoutError: await ints.channel.send('{user}, você emorou demais, bye!'.format(user=str(ints.user.mention)))
            if prefix.startswith('geral!'):
                edit["description"] = content[6:]
                await message.add_reaction('✅')
            elif prefix.startswith('url!'):
                try:
                    edit["url"] = requests.get(content[4:]).url
                    await message.add_reaction('✅')
                except:
                    await message.add_reaction('❌')
            elif prefix.startswith('> '): continue
            elif prefix == 'done':
                Resp.edit(**edit)
            elif prefix == 'dis':
                await del_messages(chr)
                await message.reply('**Todas as alterações foram descartadas**'); return
            else: chr.append(await ints.channel.send('**. . .**'))
            chr.append(message)
async def del_messages(chr: list):
    for i in chr:
        try: await i.delete()
        except: ...
    return
def RespsFmt(directory: str, Str: str='') -> discord.Embed:
    for i in utilz.all_respirations(directorys=[directory]):
        Str = '{Str}**{name}** -> **{forms}** forms, Command: **`/respiration {command}`**\n'.format(Str=Str, name=str(i).title(), forms=str(len(i.forms)), command=str(i))
    return discord.Embed(
        title='Respirações',
        description=str(Str),
        colour=0x9B59B6
    ).set_image(url='https://c.tenor.com/kIq0iqKuzA8AAAAC/hashira.gif').set_footer(text='{} Resps, all-forms'.format(str(len(utilz.all_respirations(directorys=[directory]))))) 
class myButtom(discord.ui.View):
    def __init__(self, List: list[discord.Embed], ints: discord.Interaction):
        super().__init__(timeout=20)
        self.value = None
        self.embeds = List
        self.lenght = len(self.embeds)
        self.i = 0
        self.ints = ints
    @discord.ui.button(label='Back Page', style=discord.ButtonStyle.grey)
    async def BackPage(self, ints: discord.Interaction, button: discord.ui.Button):
        if not self.i-1 == -1: self.i -= 1
        else: self.i = self.lenght-1
        await ints.response.edit_message(embed=self.embeds[self.i])
        self.ints = ints
    @discord.ui.button(label='Next Page', style=discord.ButtonStyle.grey)
    async def NextPage(self, ints: discord.Interaction, button: discord.ui.Button):
        if self.i + 1 < self.lenght: self.i += 1
        else: self.i = 0
        await ints.response.edit_message(embed=self.embeds[self.i])
        self.ints = ints
    async def on_timeout(self) -> None:
        self.clear_items()
        self.stop()
async def setup(bot: commands.Bot):
    await bot.add_cog(Respiration(bot), guilds=[discord.Object(id=971803172056219728), discord.Object(id=971171026702598165)])