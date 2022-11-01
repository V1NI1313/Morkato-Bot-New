from discord.ext import commands
from discord import app_commands
import discord
import utilz
### -> Exceptions <- ###
from utilz.errors import PlayerMappedBreed, GuildAlredyExists, GuildNotExist

class Player(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="register", description="Registra o usuário")
    async def register(self, ints: discord.Interaction, name: str) -> None:
        try: Guild = utilz.Guild(ints.guild)
        except GuildNotExist: Guild = utilz.New_Guild(ints.guild)
        try: Player = Guild.players.new(ints.user, nick=name.lower().title())
        except PlayerMappedBreed: await ints.response.send_message("**O cara é híbrido, humano e oni... Tá certo isso?**"); return
        await ints.response.send_message("Guild: {guild} Player: {player}".format(guild=Guild, player=Player))
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Player(bot), guild=discord.Object(id=1030300817175089203))