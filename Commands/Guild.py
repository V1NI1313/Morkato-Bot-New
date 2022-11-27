from discord.ext import commands
import discord
import utilz

class Guild(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(name="tesrGuild")
  async def Guild(self, ctx: commands.Context) -> None:
    await ctx.reply(f"`{utilz.Guild.from_guild(ctx.guild)}`")
  @commands.command(name="configure-guild")
  async def Configure_Guild(
    self,
    ctx: commands.Context,
    human: discord.Role,
    oni: discord.Role,
    hybrid: discord.Role,
    separator: commands.Greedy[discord.Role]
  ) -> None:
    Guild = utilz.New_Guild(
      ctx.guild,
      human,
      oni,
      hybrid,
      separator
    )
    await ctx.reply(f"`{Guild}`")
    
async def setup(bot: commands.Bot) -> None:
  return await bot.add_cog(Guild(bot))