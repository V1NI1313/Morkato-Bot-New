from discord.ext import commands
import discord
import utilz
### -> Exceprions <- ###
from utilz.errors import UserNotExists

class Family(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command("family")
  async def Family(self, ctx: commands.Context) -> None:
    Guild = utilz.Guild.from_guild(ctx.guild)
    user = Guild.users.get(ctx.author.id)
    if user is None or user.breed is None:
      await ctx.reply("**Para usar esse comando, você terá que dar comando `!breed`**"); return
    if user.rolls_familys.choice == 0:
      await ctx.reply("**Você não tem mais rolls para usar!**"); return
    family = Guild.familys.random(user)
    if family is None:
      await ctx.reply("**Éh... Não ganhou nada .-.**"); return
    user.rolls_familys.add(family)
    await ctx.send(embed=family.embed())
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Family(bot))