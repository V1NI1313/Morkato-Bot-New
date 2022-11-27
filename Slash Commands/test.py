from discord.ext import commands
import discord

class Tests(commands. Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
async def setup(bot: commands.Bot) -> None:
  return await bot.add_cog(Tests(bot))