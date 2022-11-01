from discord.ext import commands
from discord import app_commands
from unidecode import unidecode
import discord
import utilz
### -> Exeptions <- ###
from utilz.errors import RespirationNotFound
from asyncio.exceptions import TimeoutError

class Kekkijutsu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name='kekkijutsu', description='Exibe informações da kekkijutsu passada')
    async def Kekkijutsu(self, ints: discord.Interaction, kekki_name: str=None):
        if kekki_name is None: await ints.response.send_message(embed=KekkisFmt(directory=utilz.respiration._dirs.Kekkijutsu)); return
        try:
            Kekki = utilz.Kekkijutsu(Name=unidecode(str(kekki_name)).replace(' ', '-').lower())
            # await ctx.send(embed=KekkijutsuFormated(Kekki=Kekki))
            tesr = set_embeds(Resp=Kekki)
            if len(tesr) == 1: await ints.response.send_message(embed=tesr[0]); return
            page = 0
            msg = await ints.channel.send(embed=tesr[page])
            while True:
                await msg.add_reaction('⏮')
                await msg.add_reaction('⏭')
                try: reaction, user = await self.bot.wait_for('reaction_add', timeout=120, check=lambda reaction, user: user.id == ints.user.id)
                except TimeoutError: return
                if str(reaction.emoji) == '⏮' and not page-1== -1: page -= 1
                elif str(reaction.emoji) == '⏭' and not page+1 >= len(tesr): page += 1
                await msg.edit(embed=tesr[page])
                await msg.remove_reaction(emoji=str(reaction.emoji), member=ints.user)
        except RespirationNotFound: await ints.response.send_message('__**Cá estou eu, no meio no deserto procurando essa kekkijutsu, sem água e sem vida**__')

def KekkisFmt(directory, Str: str='') -> discord.Embed:
    for i in utilz.all_respirations(directory=directory):
        Str = '{Str}**{name}** -> **{forms}** forms, Command: **`!kekkijutsu {command}`**\n'.format(Str=Str,name=str(i.name).title(), forms=str(len(i.forms)), command=str(i.name))
    return discord.Embed(
        title='Kekkijutsu',
        description=str(Str) if not Str == '' else 'No Kekkijutsu',
        colour=0x9B59B6
    ).set_footer(text='{} Kekki`s, all-forms'.format(str(len(utilz.all_respirations(directory=directory))))).set_image(url='https://c.tenor.com/7x4O6yBgF10AAAAC/kimetsu-no-yaiba-demon-slayer.gif')

def KekkijutsuFormated(Kekki: utilz.Kekkijutsu):
    Embed = discord.Embed(
        title=str(Kekki.name).lower().title(),
        description=str(Kekki.description) + '\n\n**✦ ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ・あ・⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ✦**',
        colour=0x9B59B6
    )
    Str_Fmt = ['**{extend}:** /a {form} `{fsk}`'.format(extend=i.extend, form=i.name.title(), fsk=str(r'**kwargs')) for i in Kekki.forms]
    Embed.add_field(name='Commandos', value='\n'.join(Str_Fmt), inline=False)
    if not Kekki.url is None: Embed.set_image(url=Kekki.url)
    return Embed

def set_embeds(Resp: utilz.Respiration) -> list:
    ks = [Resp.forms[i:i + 10] for i in range(0, len(Resp.forms), 10)]
    embeds = []
    for g, h in enumerate(ks):
        embeds.append(discord.Embed(title=str(Resp.name).lower().title(), description=str(Resp.description) + '\n\n**✦ ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ・あ・⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ✦**', colour=0x9B59B6))
        Str_Fmt = ['**{extend}:** /a {form} `{fsk}`'.format(extend=i.extend, form=i.name.title(), fsk=str(r'**kwargs')) for i in h]
        embeds[g].add_field(name='Comandos\nㅤ', value='\n'.join(Str_Fmt), inline=False).set_footer(text='page {} / {}'.format(g+1, len(ks)))
        if not Resp.url is None: embeds[g].set_image(url=Resp.url)
    return embeds
async def setup(bot: commands.Bot):
    await bot.add_cog(Kekkijutsu(bot), guilds=[discord.Object(id=971803172056219728), discord.Object(id=971171026702598165)])
