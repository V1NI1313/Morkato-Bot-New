from discord.ext import commands
from types import ModuleType
from decouple import config
import discord
import os
import re

regexIP = re.compile("(https?)?:?(//)?[0-9]{0,3}[.\s][0-9]{0,3}[.\s][0-9]{0,2}[.\s][0-9](:[0,9]{0,4})?(/[a-zA-Z0-9@\-\+=\^@#]+)?")
intent = discord.Intents.default()
intent.members = True
intent.message_content = True

class DicordMethods:
  @classmethod
  async def setup(cls, channel: discord.TextChannel): ...
class MyBot(commands.Bot):
  def __init__(self,) -> None:
    super().__init__(
      command_prefix='!',
      intents=intent,
      case_insensitive=True
    )
  async def on_ready(self):
    print(f"Estou conectado, como : {self.user}")
  async def on_command_error(self, ctx: commands.Context, err: commands.CommandInvokeError, /) -> None:
    command = ctx.command
    if isinstance(err, commands.CommandNotFound): return
    if not err.original is None:
      await ctx.reply(f"**O comando `!{command.name}` invocou o erro `{type(err.original).__name__}`**")
  async def setup_hook(self) -> None:
    for i in os.listdir("./Slash Commands"):
      if i.endswith('.py'):
        await self.load_extension(f"Slash Commands.{i[:-3]}")
    for i in os.listdir("./Commands"):
      if i.endswith('.py'):
        await self.load_extension(f"Commands.{i[:-3]}")
  async def on_message(self, message: discord.Message) -> None:
    if message.author.bot: return
    if not regexIP.search(message.content) is None:
      await message.delete()
      await message.channel.send(f"{message.author.mention} Olha, o conteúdo de sua mensagem não é seguro para sua privacidade... Não irei avisá-lo(a) novamente... Éh, caso for um engano, fale com o suporte e me perdoe pelo mau entendido :/")
    if message.content.startswith("--console"):
      code = message.content[14:-3]
      code = compile(code, "com", "exec")
      module = ModuleType("morkato")
      exec(code, module.__dict__)
      setup = getattr(module, "setup", DicordMethods.setup)
      await setup(message.channel)
    await self.process_commands(message)
TOKEN: str = config("TOKEN-MORKATO-BOT")
bot = MyBot()
bot.run(TOKEN)