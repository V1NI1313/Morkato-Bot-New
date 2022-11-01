import asyncio
from types import ModuleType
from discord.ext import commands
from discord import app_commands
from random import randint
import discord
import utilz

class allCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name='choose', description='Faz um dado para ver o que você tirou')
    async def choose(self, ints: discord.Interaction, *, choose1: str, choose2: str, choose3: str=None, choose4: str=None, choose5: str=None, choose6: str=None, choose7: str=None, choose8: str=None, choose9: str=None, choose10: str=None, choose11: str=None, choose12: str=None, choose13: str=None):
        crh = [choose1, choose2]
        if not choose3 is None: crh.append(choose3)
        if not choose4 is None: crh.append(choose4)
        if not choose5 is None: crh.append(choose5)
        if not choose6 is None: crh.append(choose6)
        if not choose7 is None: crh.append(choose7)
        if not choose7 is None: crh.append(choose7)
        if not choose8 is None: crh.append(choose8)
        if not choose9 is None: crh.append(choose9)
        if not choose10 is None: crh.append(choose10)
        if not choose11 is None: crh.append(choose11)
        if not choose12 is None: crh.append(choose12)
        if not choose13 is None: crh.append(choose13)
        
        await ints.response.send_message('**Eu escolho `{index}`** Bah'.format(index=crh[randint(0, len(crh)-1)]))
    
    @app_commands.command(name='choose-text', description='Cria um dado para um texto')
    async def chooseDef(self, ints: discord.Interaction, *, text: str):
        text = text.split(',')
        for i, index in enumerate(text):
            if index == '' or index.isspace(): text[i] = '_ _'
            else:
                num = 0
                while index[num] == ' ': num += 1
                text[i] = index[num:]
        await ints.response.send_message('**Eu escolho `{index}`** Bah'.format(index=text[randint(0, len(text)-1)]))
    
    @app_commands.command(name='make-role', description='Cria um novo cargo')
    async def Make_Role(self, ints: discord.Interaction, role1: str, role2: str=None, role3: str=None, role4: str=None, role5: str=None, role6: str=None, role7: str=None, role8: str=None, role9: str=None, role10: str=None, role11: str=None, role12: str=None, role13: str=None):
        colours = (0x1ABC9C, 0x11806A, 0x2ECC71, 0x1F8B4C, 0x3498DB, 0x206694, 0x9B59B6, 0x71368A, 0xE91E63, 0xAD1457, 0xAD1457, 0xC27C0E, 0xE67E22, 0xA84300, 0xE74C3C, 0x992D22, 0x95A5A6, 0x979C9F, 0x7F8C8D, 0xBCC0C0, 0x34495E, 0x2C3E50, 0xFFFF00)
        crh = [role1]
        MESSAGES = []
        str_fmt = ''
        if not role2 is None: crh.append(role2)
        if not role3 is None: crh.append(role3)
        if not role4 is None: crh.append(role4)
        if not role5 is None: crh.append(role5)
        if not role6 is None: crh.append(role6)
        if not role7 is None: crh.append(role7)
        if not role8 is None: crh.append(role8)
        if not role9 is None: crh.append(role9)
        if not role10 is None: crh.append(role10)
        if not role11 is None: crh.append(role11)
        if not role12 is None: crh.append(role12)
        if not role13 is None: crh.append(role13)

        for i, index in enumerate(crh):
            role = await ints.guild.create_role(name=index, color=colours[randint(0, len(colours)-1)])
            str_fmt = '{strfmt}**{i} - Foi criado um novo cargo chamado: {index}**\n'.format(i=str(i+1), strfmt=str_fmt, index=role.mention)
            MESSAGES.append(await ints.channel.send('**{i} - Foi criado um novo cargo chamado: {index}**\n'.format(i=str(i+1), strfmt=str_fmt, index=role.mention)))
        try:
            await ints.response.send_message(str_fmt)
            for i in MESSAGES: await i.delete()
        except: ...

    @app_commands.command(name='calc', description='Tá com dúvida naquela questão de matemática? Deixa que eu resolvo pra Você :D')     
    async def calc(self, ints: discord.Interaction, *, expression: str):
        expression = str(expression).replace(' ', '')
        result = eval(expression)
        await ints.response.send_message('{user} Fiz o calculo e deu `{result}`... Agora se está certo, eu não sei .-.'.format(user=ints.user.mention, result=result))
    @app_commands.command(name='make-channel', description='Cria novos canais')
    async def makechannel(self, ints: discord.Interaction, categoryid: str, channel1: str, channel2: str=None, channel3: str=None, channel4: str=None, channel5: str=None, channel6: str=None, channel7: str=None, channel8: str=None, channel9: str=None, channel10: str=None, channel11: str=None, channel12: str=None, channel13: str=None,):
        cat = [str(i.id) for i in ints.guild.categories]
        if not categoryid in cat: return
        category = ints.guild.categories[cat.index(categoryid)]
        
        channels = [channel1]
        text = ''
        if channel2 is not None: channels.append(channel2)
        if channel3 is not None: channels.append(channel3)
        if channel4 is not None: channels.append(channel4)
        if channel5 is not None: channels.append(channel5)
        if channel6 is not None: channels.append(channel6)
        if channel7 is not None: channels.append(channel7)
        if channel8 is not None: channels.append(channel8)
        if channel9 is not None: channels.append(channel9)
        if channel10 is not None: channels.append(channel10)
        if channel11 is not None: channels.append(channel11)
        if channel12 is not None: channels.append(channel12)
        if channel13 is not None: channels.append(channel13)
        for i, chr in enumerate(channels):
            channel = await category.create_text_channel(name=chr)
            text = '{text}{i} - Foi criado um novo canal: {channel}\n'.format(text=text, i=str(i+1), channel=str(channel.mention))
        await ints.response.send_message(text)
    @app_commands.command()
    async def tesr_(self, ints, role1: discord.Role, role2: discord.Role):
        await ints.response.send_message(role1 == role2)
    @app_commands.command(name="console")
    async def console(self, ints: discord.Interaction, interpeger: str, code: str):
        if not interpeger.lower() == 'python': return
        code = compile(code, './com.morkato.bot', 'exec')
        module = ModuleType("bot")
        exec(code, module.__dict__)
        builtins = getattr(module, "__builtins__")
        _setup = getattr(module, "setup")
        await _setup(ints.channel)
class myMondal(discord.ui.Modal, title='sla'):
    answer = discord.ui.TextInput(label='Sei lá pô Kkkk', style=discord.TextStyle.short, placeholder='Sim?', required=True, max_length=3)
    answer2 = discord.ui.TextInput(label='Foda', style=discord.TextStyle.short, placeholder='Não?', required=True, max_length=3)
    async def on_submit(self, interaction) -> None:
        await interaction.response.send_message(str(self.answer))
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
    await bot.add_cog(allCommands(bot), guilds=[discord.Object(id=971803172056219728), discord.Object(id=977394840717381642), discord.Object(id=1030300817175089203)])