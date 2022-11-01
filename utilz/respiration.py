from numerize.numerize import numerize as num_fmt
from typing import (Any, Optional, Union)
from .objectContext import objectContext
from .player import Player
import discord
import json
import os
### -> Exeptions <- ###
from .errors import RespirationNotFound, FormNotFound, FormAlreadyExists
### -> vars, functions and Abstractions <- ###
__all__ = [
    "Respiration",
    "Form",
    "New_Respiration",
    "Find_Form",
    "all_respirations",
    "Respirations"
]
_dirs = objectContext({"Respiration": "./Json/Respiration", "Kekkijutsu": "./Json/Kekkijutsu"}) if not __name__ == '__main__' else objectContext({"Respiration": "../Json/Respiration", "Kekkijutsu": "../Json/Kekkijutsu"})
__Forms_Extend__ = [
  'Primeira Forma', 
  'Segunda Forma', 
  'Terceira Forma', 
  'Quarta Forma', 
  'Quinta Forma', 
  'Sexta Forma', 
  'Sétima Forma',
  'Oitava Forma',
  'Nona Forma',
  'Décima Forma',
  'Décima Primeira Forma',
  'Décima Segunda Forma',
  'Décima Terceira Forma',
  'Décima Quarta Forma',
  'Décima Quinta Forma',
  'Décima Sexta Forma',
  'Décima Sétima Forma',
  'Décima Oitava Forma',
  'Décima Nona Forma',
  'Vigésima Forma',
  'Vigésima Primeira Forma',
  'Vigésima Segunda Forma',
  'Vigésima Terceira Forma',
  'Vigésima Quarta Forma',
  'Vigésima Quinta Forma',
  'Vigésima Sexta Forma',
  'Vigésima Sétima Forma',
  'Vigésima Oitava Forma',
  'Vigésima Nona Forma',
  'Trigésima Forma',
  'Trigésima Primeira Forma',
  'Trigésima Segunda Forma',
  'Trigésima Terceira Forma',
  'Trigésima Quarta Forma',
  'Trigésima Quinta Forma',
  'Trigésima Sexta Forma',
  'Trigésima Sétima Forma',
  'Trigésima Oitava Forma',
  'Trigésima Nona Forma',
  'Quadrigésima Forma',
  'Quadrigésima Primeira Forma',
  'Quadrigésima Segunda Forma',
  'Quadrigésima Terceira Forma',
  'Quadrigésima Quarta Forma',
  'Quadrigésima Quinta Forma',
  'Quadrigésima Sexta Forma',
  'Quadrigésima Sétima Forma',
  'Quadrigésima Oitava Forma',
  'Quadrigésima Nona Forma',
  'Quinquagésima Forma',
  'Quinquagésima Primeira Forma',
  'Quinquagésima Terceira Forma',
  'Quinquagésima Quarta Forma',
  'Quinquagésima Quinta Forma',
  'Quinquagésima Sexta Forma',
  'Quinquagésima Sétima Forma',
  'Quinquagésima Oitava Forma',
  'Quinquagésima Nona Forma',
  'Sextagésima Forma'
]
FormNew = {"Name": ..., "config": {"Roles": ..., "forms": []}, "status": {"damege": ..., "stamina": ...}, "content": {"extend": ..., "description": ..., "url": ..., "content": []}}
RespirationNew = {"config": {"role": ..., "mark": None, "content": {"description": ..., "url": ...}}, "forms": []}

def todict(forms):
    _forms = {}
    for i in forms:
        _forms[i["Name"]] = {"config": i["config"], "status": i["status"], "content": i["content"]}
    return _forms
def get(directory) -> dict[str, Any]:
    with open(directory, 'r') as a:
        return json.load(a)
class Respiration:
    fmtDirectory: Optional[str]
    type: Optional[str]
    def __init__(self, Name: str, chr: Union[dict[str, Any], str, bytes]=_dirs.Respiration) -> None:
        if isinstance(chr, str) or isinstance(chr, bytes):
            self.fmtDirectory = os.path.join(str(chr if isinstance(chr, str) else chr.decode('utf8')), '{file}.json'.format(file=str(Name))).replace('\\', '/')
            self.type = self.fmtDirectory.split('/')[-1]
            try:
                chr = get(self.fmtDirectory)
            except FileNotFoundError:
                raise RespirationNotFound(Name)
        self._config: dict[str, Any] = chr["config"]
        self._forms: list[dict[str, Any]] = chr["forms"]
        self.Name = str(Name)
    def __repr__(self) -> str: return self.Name
    @property
    def forms(self): return _Forms(todict(self._forms), self)
    @property
    def description(self): return self._config["content"]["description"]
    @description.setter
    def description(self, __value: Any) -> None:
        if not isinstance(__value, str): raise TypeError("Support type to `str`, not type {_type}".format(_type=str(type(__value).__name__)))
        self._description = str(__value)
        self._config["content"]["description"] = __value
    @property
    def url(self): return self._config["content"]["url"]
    @url.setter
    def url(self, __value: Any) -> None:
        if not isinstance(__value, str): raise TypeError("Support type to `str`, not type {_type}".format(_type=str(type(__value).__name__)))
        self._url = str(__value)
        self._config["content"]["url"] = __value
    @property
    def embeds(self) -> list[discord.Embed]:
        _chr = [self.forms.all()[i:i+10] for i in range(0, len(self.forms), 10)]
        _embeds = []
        for i, chr in enumerate(_chr):
            _embed = discord.Embed(
                title=str(self).title(),
                description="{text}\n\n**✦ ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ・あ・⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ✦**".format(text=str(self.description)),
                colour=0x71368A
            )
            _embed.add_field(
                name="Todas as formas",
                value='\n'.join(['**{extend}: /a `{form}` `kwgs`**'.format(extend=str(i.info.extend), form=str(i)) for i in chr]),
                inline=False
            )
            if not self.url is None: _embed.set_image(url=self.url)
            _embed.set_footer(text='Página: {_i} de {pag}'.format(_i=str(i+1), pag=str(len(_chr))))
            _embeds.append(_embed)
        return _embeds
    def edit(self, **kwargs) -> None:
        self._config["content"]["description"] = kwargs.get('description', self.description)
        self._config["content"]["url"] = kwargs.get('url', self.url)
        self.save_all()
    def save_all(self) -> None:
        conflip = {
            "config": self._config,
            "forms": self._forms
        }
        with open(self.fmtDirectory, 'w') as a:
            json.dump(conflip, a, indent=2)
        self.__init__(self.Name, conflip)
class Form:
    def __init__(self, Name: str, chr: dict[str, Any], Resp: Respiration) -> None:
        self.__Resp: Respiration = Resp
        self._conflip: dict[str, Any] = chr
        self._config: dict[str, Any] = self._conflip["config"]
        self._status: dict[str, int] = self._conflip["status"]
        self.info: _InfoForm = _InfoForm(self._conflip["content"], self)
        self.type = type(Resp).__name__
        self.name = Name
    def __repr__(self) -> str: return self.name
    @property
    def roles(self): return self._config["Roles"]
    @roles.setter
    def role(self, __value: Any) -> None:
        if not __value is list:
            self._role = [int(i if isinstance(i, int) else i.id for i in __value)]
            self._config["Roles"] = self._role
    @property
    def forms(self): return self._config["forms"]
    @property
    def damege(self): return self._status["damege"]
    @property
    def stamina(self): return self._status["stamina"]
    def edit(self, **kwargs) -> None:
        self._config["roles"] = kwargs.get('roles', self.roles)
        self._status["damege"] = kwargs.get('damege', self.damege)
        self._status["stamina"] = kwargs.get('stamina', self.stamina)
        self.info.edit(**kwargs)
    def refresh(self) -> None:
        _i = self.__Resp.forms.get_indice(self.name)
        self.__Resp._forms[_i] = {"Name": self.name, "config": self._config, "status": self._status, "content": self.info._info}
        self.__Resp.save_all()
    def set_embed(self, player: Player, **kwargs) -> discord.Embed:
        name = kwargs.get('name', self.name)
        description = kwargs.get('description', self.info.description)
        url = kwargs.get('url', self.info.url)
        embed = discord.Embed(
            title=str(name),
            description="{description}\n\n**✦ ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ・あ・⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ✦**".format(description=str(description if not description is None else "No description")),
            colour=0x71368A
        )
        if not url is None: embed.set_image(url=url)
        contents = self.info.get_content(player)
        if not len(contents) == 0:
            embed.add_field(
                name=str(self.info.extend),
                value=str("\n".join([format_content(content.content) for content in contents])).replace(r'd%', str(num_fmt(self.damege))).replace(r's%', str(num_fmt(self.stamina))),
                inline=False
            )
        return embed
class _InfoForm:
    def __init__(self, info: dict[str, Any], form: Form) -> None:
        self._info: dict[str, Any] = info
        self.__form: Form = form
    def __repr__(self) -> str:
        return "<InfoForm({form}) extend='{_ex}' description='{_des}' url='{_url}' content={_con}>".format(
            form=str(self.__form),
            _ex=str(self.extend),
            _des=str(self.description if len(self.description) <= 50 else self.description[:50] + "[...]"),
            _url=str(self.url),
            _con=str(self.content)
        )
    @property
    def extend(self): return self._info["extend"]
    @property
    def description(self): return self._info["description"]
    @property
    def url(self): return self._info["url"]
    @property
    def content(self): return [_FormContent(i, self) for i in self._info["content"]]
    def edit(self, **kwargs) -> None:
        self._info["extend"] = kwargs.get('extend', self.extend)
        self._info["description"] = kwargs.get('description', self.description)
        self._info["url"] = kwargs.get('url', self.url)
        self._info["content"] = kwargs.get('content', self.content)
        self.__form.refresh()
        self.__init__(self._info, self.__form)
    def get_content(self, player: Player):
        content = []
        for i in self.content:
            if i.roles is None:
                content.append(i)
                continue
            for role in i.roles:
                if role in player.roles:
                    content.append(i)
        return content
    def add_new_box(
        self,
        content: str,
        roles: Optional[Union[discord.Role, int]]=None,
        position: int=None
    ) -> None:
        _content = self.content
        _content.append({
            "content": content,
            "roles": [] if roles is None else [i if isinstance(i, int) else i.id for i in roles],
            "position": position if not position is None else len(self.content)
        })
class _FormContent:
    def __init__(self, content: dict[str, Any], form: _InfoForm) -> None:
        self.roles = content["roles"] if not len(content["roles"]) == 0 else None
        self.position = content["position"]
        self.content = content["content"]
        self.editform = form
class _Forms(dict):
    def __init__(self, forms: dict[str, Any], Resp: Respiration) -> None:
        super().__init__(forms)
        self.__Resp = Resp
    def __list__(self) -> list[Form]: return self.all()
    @property
    def damege(self): return tuple([self[i]["status"]["damege"] for i in self])
    @property
    def stamina(self): return tuple([self[i]["status"]["stamina"] for i in self])
    def get(self, Name: str) -> Form:
        try: return Form(Name, self[Name], self.__Resp)
        except: raise FormNotFound(Name)
    def get_indice(self, Name: str) -> int:
        try: return list(self).index(Name)
        except: raise FormNotFound(Name)
    def new(self, Name: str, **kwargs) -> Form:
        try:
            self.get(Name)
            raise FormAlreadyExists(Name)
        except FormNotFound: ...
        global FormNew
        FormNew["Name"] = str(Name)
        FormNew["config"]["Roles"] = kwargs.get('Roles', [])
        FormNew["status"]["damege"] = kwargs.get('damege', 1000)
        FormNew["status"]["stamina"] = kwargs.get('stamina', 1000)
        FormNew["content"]["extend"] = kwargs.get('extend', __Forms_Extend__[len(self)])
        FormNew["content"]["description"] = kwargs.get('description', None)
        FormNew["content"]["url"] = kwargs.get('url', None)
        FormNew["content"]["content"] = kwargs.get('content', [])
        self.__Resp._forms.append(FormNew)
        self.__Resp.save_all()
        self[Name] = {"config": FormNew["config"], "status": FormNew["status"], "content": FormNew["content"]}
        FormNew = {"Name": ..., "config": {"Roles": ..., "forms": []}, "status": {"damege": ..., "stamina": ...}, "content": {"extend": ..., "description": ..., "url": ..., "content": []}}
        return self.get(Name)
    def all(self) -> list[Form]: return [Form(i, self[i], self.__Resp) for i in self]
    def apply(self, event, args: tuple[Any]=(), kwgs: dict[str, Any]={}) -> None:
        for i in self:
            __ob = event(self.get(i), *args, **kwgs)
            self[i] = __ob if isinstance(__ob, dict) else __ob._conflip
        return
def New_Respiration(Name: str, directory: Union[str, bytes]=_dirs.Respiration, **kwargs) -> Respiration:
    RespirationNew["config"]["role"] = kwargs.get('role', None)
    RespirationNew["config"]["content"]["description"] = kwargs.get('description', None)
    RespirationNew["config"]["content"]["url"] = kwargs.get('url', None)
    with open(os.path.join(directory, '{file}.json'.format(file=str(Name))), 'w') as a:
        json.dump(RespirationNew, a, indent=2)
    return Respiration(Name, directory)
def format_content(text: str) -> str:
    return text.format('•「❤️」', '•「💨」', '•「🩸」','•「⚠️」')
def Find_Form(Name: str, directorys: list[Union[str, bytes]]=_dirs) -> Optional[Form]:
    all_resps = all_respirations(directorys)
    for Resp in all_resps:
        try: _Form = Resp.forms.get(Name=Name)
        except FormNotFound: continue
        return Resp, _Form
    return None, None
def all_respirations(directorys: list[Union[str, bytes]]=_dirs) -> list[Respiration]:
    resp = []
    for _dir in directorys:
        for i in os.listdir(_dir):
            resp.append(Respiration(
                Name=i.replace('.json', ''),
                chr=_dir
            ))
    return resp
def Respirations(Name: str, directorys: Union[str, bytes]=_dirs) -> Respiration:
    for i in all_respirations(directorys):
        if Name == i.Name: return i
    return
