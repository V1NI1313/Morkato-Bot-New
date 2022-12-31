from discord.ext import commands
from utilz import utils
import discord
import utilz
import re
### -> Exceprions <- ###
from utilz.errors import UserNotExists

regex = re.compile("@(?P<key>[a-zA-Z0-9_\-\+\=\$]+) ?\"(?P<value>[a-zA-Z0-9_\-\+\=\$\s]+)\"")
embed = discord.Embed(
  title="Breed",
  description="A raça é um conceito de classificação que obedece alguns parâmetros para categorizar diferentes populações de uma mesma espécie biológica de acordo com suas características genéticas ou fenotípicas.",
  colour=0x71368A
)
embed.add_field(name="Escolhas:", value="**`🧑` - Humano\n`👹` - Oni**")
async def PlayerBreedChoice(ctx: commands.Context, guild: utilz.Guild, Player: utilz.User) -> None:
  if not Player.breed is None and not  guild.players.get(Player.id) is None:
    await ctx.reply("**Você nn pode ficar mudando de raça do nada**"); return
  message = await ctx.send(embed=embed)
  await message.add_reaction('🧑')
  await message.add_reaction('👹')
  def check(reaction: discord.Reaction, user: discord.User) -> bool:
    return (
      user.id == ctx.author.id
      and reaction.message.guild.id == ctx.guild.id
      and reaction.message.channel.id == ctx.channel.id
      and reaction.message.id == message.id
    )
  try: reaction, user = await ctx.bot.wait_for("reaction_add", timeout=20, check=check)
  except TimeoutError: return
  if str(reaction.emoji) == '🧑': choice = 1
  elif str(reaction.emoji) == '👹': choice = 2
  else: return
  if choice == 1 and guild.human_role is not None:
    await Player.auth.add_roles(guild.human_role)
  elif choice == 2 and guild.oni_role is not None:
    await Player.auth.add_roles(guild.oni_role)
  Player.edit(breed=choice)
  await message.reply("**Tudo certo chefe! Salvei aqui.**")
class Player(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(aliases=["Raça", "Raca"])
  async def Breed(self, ctx: commands.Context) -> None:
    Guild = utilz.Guild.from_guild(ctx.guild)
    user = Guild.users.get(ctx.author.id)
    if user is None:
      user = Guild.users.new(ctx.author)
    switch = utils.Switch(user.breed)
    if switch(1) and Guild.human_role is not None:
      await ctx.send("**ALERT: Parece que sua raça atual não tem cargo. Pessa pra um adm criar o cargo para humano!**")
    elif switch(2) and Guild.oni_role is not None:
      await ctx.send("**ALERT: Parece que sua raça atual não tem cargo. Pessa pra um adm criar o cargo para oni!**")
    switch = utils.Switch(Guild.settings.playerBreed)
    if switch(0): await PlayerBreedChoice(ctx, Guild, user)
  @commands.command(aliases=["Registrar"])
  async def Register(self, ctx: commands.Context, *, json: str) -> None:
      Guild = utilz.Guild.from_guild(ctx.guild)
      user = Guild.users.get(ctx.author.id)
      if user is None or user.breed is None:
        await ctx.reply("**Para usar esse comando, você terá que dar comando `!breed`**"); return
      elif not Guild.players.get(user.id) is None:
        await ctx.send("**Você já está registrado!**"); return
      elif not len(user.rolls_familys):
        await ctx.reply("**Para usar esse comando, você terá que dar comando `!family**"); return
      args = dict(map(lambda elem: (elem["key"], elem["value"]),  regex.finditer(json)))
      if args.get("name") is None or args.get("age") is None:
        await ctx.send("**Você tem que passar os parâmetros .-. É assim: `!register @name \"foo\" @age \"1234567890\"` também pode usar o parâmetro opcional que é `@surname \"foo\"`**"); return
      names = map(lambda elem: f"`{elem.name}`", map(lambda elem: elem[0], user.rolls_familys))
      embed = discord.Embed(
        title="Family",
        description="**Escolha sua família:\n\n{0}**".format('\n'.join(map(lambda elem: f"{elem[0]} - {elem[1]}", enumerate(names, start=1))))
      )
      await ctx.send(embed=embed)
      def check(message: discord.Message) -> bool:
        return (
          message.author.id == ctx.author.id
          and message.guild.id == ctx.guild.id
          and message.channel.id == ctx.channel.id
        )
      try: message: discord.Message = await self.bot.wait_for("message", timeout=120, check=check)
      except TimeoutError: ctx.reply("**Timeout**"); return
      try: opt = int(message.content.strip())
      except: await ctx.send("**Algo deu errado**"); return
      if opt > len(user.rolls_familys):
        await ctx.send(f"**O número não pode ser maior que `{len(user.rolls_familys)}`**"); return
      elif opt <= 0:
        await ctx.send(f"**O número não pode ser menor ou igual à `0`**"); return
      args["family"] = user.rolls_familys[opt][0]
      Guild.players.new(user, **args)
      await ctx.reply("**Você foi registrado com sucesso!**")
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Player(bot))