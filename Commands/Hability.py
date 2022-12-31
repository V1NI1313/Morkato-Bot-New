from discord.ext import commands
from typing import Union
import discord
import utilz
### -> Exceptions <- ###
from utilz.errors import UserNotExists

embed = discord.Embed(
  title="Create Variable",
  description="**-> Como funciona?\n\n\t- Usando um script externo próprio de seu servidor você poderá fazer várias formatações de texto.\n\n-> Como faço isso?\n\n\t- Pegando um script externo de seu servidor, como por exmplo. Tenho um que se chama `test` ```py\ndef upper(this):\n  return this.upper()```\n\n\t- Esse script transforma todas as letras em maiúsculas... Mas não precisa se preocupar, já tem um script desse imbutido kk\n\n-> Como posso chamá-lo?\n\n\t- Para chamá-lo é simples, só colocar a variável entre chaves, exemplo `${\"test\"::upper(this)}` output ```TEST``` **",
  colour=0x71368A
)

class Hability(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(aliases=["Habilidade"])
  async def Hability(self, ctx: commands.Context) -> None:
    Guild = utilz.Guild.from_guild(ctx.guild)
    user = Guild.users.get(ctx.author.id)
    if user is None or user.breed is None:
      await ctx.reply("**Para usar esse comando, você terá que dar comando `!breed`**"); return
    if user.rolls_habilitys.choice == 0:
      await ctx.reply("**Você não tem mais rolls de habilidade!**"); return
    hability = Guild.habilitys.random(user)
    if hability is None:
      await ctx.reply("**Éh... Você não ganhou nada :D**"); return
    user.rolls_habilitys.add(hability)
    await ctx.send(embed=hability.embed())
  @commands.command(name="embed-hability")
  async def embedHability(self, ctx: commands.Context, hability: Union[discord.Role, str]) -> None:
    Guild = utilz.Guild.from_guild(ctx.guild)
    _hability = Guild.habilitys.get(hability)
    await ctx.send(embed=_hability.embed())
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Hability(bot))