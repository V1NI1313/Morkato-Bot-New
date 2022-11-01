from discord.ext import commands
from discord import app_commands
import discord

class allCommandsCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    @commands.command(name='prefix')
    async def prefix(self, ctx: commands.Context):
        await ctx.reply("Hello!")
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(allCommandsCommand(bot), guilds=[discord.Object(id=958418015576285194)])
