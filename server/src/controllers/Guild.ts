import { Response, Request } from 'express'
import { Guild, New_Guild, byID } from '../../utils/Guild'

export function getGuild(req: Request, res: Response): void {
  let guild: Guild; try {
    guild = byID(req.params.id)
    res.status(200)
    .json(guild.parse())
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}
export function newGuild(req: Request, res: Response): void {
  let guild: Guild; try {
    guild = byID(req.params.id)
    res.status(403)
    .json({"message": "GuildAlreadyExists", "status": "403"})
  } catch {
    guild = New_Guild(req.params.id, req.body)
    res.status(200)
    .json(guild.parse())
  }
}