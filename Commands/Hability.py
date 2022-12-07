from discord.ext import commands
from typing import Union
import discord
import utilz

class Hability(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(name="embed-hability")
  async def embedHability(self, ctx: commands.Context, hability: Union[discord.Role, str]) -> None:
    Guild = utilz.Guild.from_guild(ctx.guild)
    _hability = Guild.habilitys.get(hability)
    await ctx.send(embed=_hability.embed())
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Hability(bot))