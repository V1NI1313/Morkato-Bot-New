from discord.ext import commands
from discord import (app_commands, ui)
from typing import (Union)
import requests
import discord

class WebhookCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    @app_commands.command(name='interaction', description='Cria um usuário virtual')
    async def Interaction(self, ints: discord.Interaction) -> None:
        await ints.response.send_modal(MyInteractionMondal())
class MyInteractionMondal(ui.Modal, title='Interaction bot'):
    nameWebhook = ui.TextInput(label='Nome do Usuário/Webhook', style=discord.TextStyle.short, placeholder='Digite o Nome do Usuário/Webhook', required=True)
    urlWebhook = ui.TextInput(label='Imagem(url) do Usuário/Webhook', style=discord.TextStyle.short, placeholder='Digite a Imagem(url) do Usuário/Webhook', required=False)
    
    titleEmbed = ui.TextInput(label='Título da embed', style=discord.TextStyle.short, placeholder='Digite o título da embed', required=True, max_length=40,)
    descriptionEmbed = ui.TextInput(label='Descrição da embed', style=discord.TextStyle.long, placeholder='Digite a descrição da embed', required=True)
    urlEmbed = ui.TextInput(label='Imagem da embed', style=discord.TextStyle.short, placeholder='Digite a imagem da embed', required=False)

    async def on_submit(self, ints: discord.Interaction) -> None:
        self.urlWebhook = isNone(str(self.urlWebhook))
        if not self.urlWebhook == None:
            self.urlWebhook = requests.get(self.urlWebhook).content
        webhook = await ints.channel.create_webhook(name=str(self.nameWebhook), avatar=self.urlWebhook)
        Embed = discord.Embed(
            title=str(self.titleEmbed),
            description=str(self.descriptionEmbed),
            colour=0x71368A
        )
        if not isNone(str(self.urlEmbed)) == None: Embed.set_image(url=str(self.urlEmbed))
        await webhook.send(embed=Embed)
        await webhook.delete()
        await ints.response.send_message('A embed foi enviada!', ephemeral=True)
def isNone(text: str) -> Union[str, None]:
    text = str(text)
    if text.isspace() or text == '': return
    return text
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WebhookCommands(bot), guilds=[discord.Object(id=int(1030300817175089203))])