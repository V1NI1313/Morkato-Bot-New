class utilsError(Exception): ...
class GuildNotExists(utilsError):
  def __init__(self, Guild: object) -> None:
    super().__init__(f"Guild {Guild.id} not exists!")
class GuildAlreadyExists(utilsError):
  def __init__(self, Guild: object) -> None:
    super().__init__(f"Guild {Guild.id} already exists!")