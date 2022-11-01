from .respiration import Respiration, Form, New_Respiration, Respirations, all_respirations, Find_Form
from .mission import Mission, New_Mission, Serch_Mission, Player_Mission
from numerize.numerize import numerize as num_fmt
from .hability import Hability, New_Hability
from .objectContext import objectContext
from .player import Player, New_Player
from .guild import Guild, New_Guild
from .functions import Conflip, FormatRarety
from typing import (Any, Union)
from .npc import Npc, New_Npc
import discord
_dirs = objectContext({"Respiration": "./Json/Respiration", "Kekkijutsu": "./Json/Kekkijutsu"}) if not __name__ == '__main__' else objectContext({"Respiration": "../Json/Respiration", "Kekkijutsu": "../Json/Kekkijutsu"})
class Kekkijutsu(Respiration):
    def __init__(self, Name: str, directory: Union[str, bytes]=_dirs.Kekkijutsu) -> None:
        super().__init__(Name, directory)
def New_Kekkijutsu(Name: str, directory: Union[str, bytes]=_dirs.Kekkijutsu, **kwargs) -> Kekkijutsu:
    return New_Respiration(
        Name=Name,
        directory=directory,
        **kwargs
    )
embeds = {
    'edits': { 
        'editform': discord.Embed(
            title='Editar Form',
            description='**╰⌲ ┊ Para editar uma Forma, Você terá que dar um dos comandos abaixo\n\n╰⌲ ┊ Forma!\n┊ Troca a Forma :D\n\n╰⌲ ┊ Geral!\n┊ Troca a descrição da Forma\n\n╰⌲ ┊ url!\n┊ Troca a imagem da Forma\n┊ Pode retornar um erro caso o cliente não ache a url da imagem\n\n╰⌲ ┊ Dano!\n┊ Edita o dano da forma\n\n╰⌲ ┊ Stamina!\n┊ Edita o fôlego da forma\n\n╰⌲ ┊ Time!\n┊ Coloca tempo em uma forma**',
            colour=0x9B59B6
        ).set_footer(text='Caso queira comentar, coloque "> " no começo'),
        'editresp': discord.Embed(
            title='Editar Respiração',
            description='**╰⌲ ┊ Para editar uma Respiração, Você terá que dar um dos comandos abaixo\n\n╰⌲ ┊ Geral!\n┊ Troca a descrição da Respiração\n\n╰⌲ ┊ url!\n┊ Troca a imagem da Forma\n┊ Pode retornar um erro caso o cliente não ache a url da imagem**',
            colour=0x9B59B6
        ).set_footer(text='Caso queira comentar, coloque "> " no começo')
    },
}

notlibs = [
    '__import__',
    'all',
    'chr',
    'compile',
    'dir',
    'divmod',
    'exec',
    'globals',
    'input',
    'open',
    'quit',
    'exit'
]