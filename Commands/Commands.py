from typing import (Mapping, Sequence)
from discord.ext import commands
from types import ModuleType
import traceback
import discord
import json
import re
### -> Exceptions <- ###
from utilz.errors import ImportPermissionError

commandRe = re.compile("```(?P<key>[A-Za-z0-9]+)\n(?P<code>[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ0-9.,\(\)/\"\'\\\^\:;!@#\$%&`\*\=\+\-\<\>~\[\]\{\}$?_\s]+)```")
def __load__(
  name: str,
  globals: Mapping[str, object] | None = ...,
  locals: Mapping[str, object] | None = ...,
  fromlist: Sequence[str] = ...,
  level: int = ...
) -> ModuleType:
  if name in ["socket", "requests",]:
    raise ImportPermissionError(name)
  return __import__(name, globals, locals, fromlist, level)
async def _setup(ctx) -> None: ...
class Commands(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command("console")
  async def Console(self, ctx: commands.Context, *, code: str) -> None:
    match = commandRe.search(code)
    if match is None:
      await ctx.reply("**Não sei interpretar essa linguaregem T-T**")
    elif match.group("key") in ["py", "python"]:
      module = {"__builtins__": {"__import__": __load__, "open": open, "True": True, "False": False, "str": str, "int": int, "bool": bool, "dict": dict, "tuple": tuple, "list": list,"enumerate": enumerate, "zip": zip, "getattr": getattr, "setattr": setattr, "__build_class__": __build_class__, "__name__": __name__, "property": property, "super": super, "type": type, "map": map, "next": next}}
      try: exec(match.group("code"), module)
      except ImportPermissionError as err:
        if err.name in ["socket", "requests",]:
          await ctx.reply(f"**Para proteger a privacidade de quem está me hosteando, é impossível importar a lib `{err.name}` pois com ela da para descobrir a sua localização.**"); return
      except Exception as a:
        await ctx.reply(f"```{traceback.format_exc()}```"); return
      setup = module.get("setup", _setup)
      try: await setup(ctx)
      except Exception as a: await ctx.reply(f"```{traceback.format_exc()}```"); return
  @commands.command(name='toJson')
  async def toJson(self, ctx: commands.Context, *, args: str) -> None:
    regex = re.compile("@(?P<key>[a-zA-Z0-9_\-\+\=\$]+) ?\"(?P<value>[a-zA-Z0-9_\-\+\=\$\s]+)\"")
    response = dict([(elem.group("key"), format(elem["value"])) for elem in regex.finditer(args)])
    await ctx.send(f"```json\n{json.dumps(response, indent=2)}```")
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Commands(bot))
def format(elem: str) -> object:
  if elem == "off": return False
  elif elem == "on": return True
  elif elem == "void": return None
  else: return elem