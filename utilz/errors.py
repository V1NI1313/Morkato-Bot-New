class UtilzError(Exception):
    def __init__(self): ...

class GuildAlredyExists(Exception):
    def __init__(self, Guild) -> None:
        super().__init__("Guild {guild} already exists!".format(guild=Guild.id))
class GuildNotExist(Exception):
    def __init__(self, Guild) -> None:
        super().__init__("Guild {guild} not exist!!".format(guild=Guild.id))

class PlayerNotFound(Exception):
    def __init__(self, user):
        super().__init__('User {user} is not found.'.format(user=str(user)))

class PlayerInMission(Exception):
    def __init__(self, user: str, mission1, mission2) -> None:
        self.player = user
        self.InMission = mission1
        self.ErrorMission = mission2
        super().__init__('Player {user} in {mission2} not is possible in {mission1}'.format(user=str(user.User), mission1=str(mission1), mission2=str(mission2)))
class PlayerMappedBreed(Exception):
    def __init__(self, Member: str) -> None:
        super().__init__("Player `{player}` mapped breed".format(player=str(Member)))

class HabilityNotFound(Exception):
    def __init__(self, Name: str):
        super().__init__('Hability {hability} is not found.'.format(hability=str(Name)))
class FamilyNotFound(Exception):
    def __init__(self, arg) -> None:
        super().__init__("Family {family!r} is not found".format(family=str(arg)))

class RespirationNotFound(Exception):
    def __init__(self, resp_name: str) -> None:
        super().__init__('Respiration `{resp}` is not found'.format(resp=resp_name))

class FormNotFound(Exception):
    def __init__(self, form_name: str):
        super().__init__('Form `{form}` is not found'.format(form=form_name))
class FormAlreadyExists(Exception):
    def __init__(self, name: str):
        super().__init__('Form `{form}` already exists'.format(form=name))

class NpcNotFound(Exception):
    def __init__(self, name: str):
        super().__init__('Npc `{npc}` is not found'.format(npc=str(name)))

class MissionNotFound(Exception):
    def __init__(self, name: str) -> None:
        super().__init__('Mission `{mission}` is not found'.format(mission=str(name)))

        