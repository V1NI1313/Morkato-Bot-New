from discord.ext import commands
from decouple import config
from typing import (Any)
import discord
import utilz
import os
### -> Exceptions <- ###
from utilz.errors import NpcNotFound
from utilz.defaults import *
from types import ModuleType

intents = discord.Intents().all(); intents.guilds=True; intents.message_content = True; intents.guilds=True; intents.webhooks=True

def removeSpace(text: str) -> str:
    if text.isspace() or text == '': return text
    numInitial = 0
    numFinal = len(text)-1
    while text[numInitial] == ' ': numInitial += 1
    while text[numFinal] == ' ': numFinal -= 1
    return text[numInitial:numFinal+1]
async def npcResponse(text: str, channel: discord.TextChannel, message: discord.Message) -> None:
    if not "!" in text[:21]: return
    npc, text = text[:text.find('!')], text[text.find('!')+1:]
    try: npc = utilz.Npc(removeSpace(npc).replace(' ', '-'))
    except NpcNotFound: return
    webhook = await npc.get_webhook(channel=channel)
    await webhook.send(text)
    await webhook.delete()
    await message.delete()
class MyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='<@972193913983103056> ', intents=intents, case_insensitive=True)
    async def on_ready(self) -> None:
        await self.change_presence(
            activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name='Você pela câmera atrás do guarda roupa'), # https://discord.gg/RUkHgZZuCC
            status=discord.Status.dnd
        )
        i = discord.Object(id=1030300817175089203)
        await self.tree.sync(guild=i)
        print('Estou conectado, como : {user}'.format(user=self.user))
    async def setup_hook(self) -> Any:
        for i in os.listdir('Slash Commands'):
            if i.endswith('.py'):
                await self.load_extension('Slash Commands.{cog}'.format(cog=i[:-3]))
        for i in os.listdir('Commands'):
            if i.endswith('.py'):
                await self.load_extension('Commands.{cog}'.format(cog=i[:-3]))
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot: return
        await npcResponse(text=str(message.content), channel=message.channel, message=message)
        if message.content.startswith("repr!"):
            text = message.content[5:].__repr__()[1:-1]
            await message.reply(str({"Message_repr": text}))
TOKEN = config('TOKEN-MORKATO-BOT')
bot = MyBot()
bot.run(str(TOKEN))