import { Request, Response } from "express"
import { byID, Guild } from "../../utils/Guild"

export function getAllHabilitys(req: Request, res: Response): void {
  let guild: Guild; try {
    guild = byID(req.params.id)
    res.status(200)
    .json(guild.get_habilitys().toJson())
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}
export function getHability(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let hability = guild.get_habilitys().get(req.params.key)
    if (hability == null) {
      res.status(404)
      .json({"message": "HabilityNotExists", "status": "404"}); return
    }; res.status(200)
    .json(hability.hability_data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}
export function newHability(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let habilitys = guild.get_habilitys()
    if (req.body == undefined || req.body["name"] !== undefined) {
      res.status(403)
      .json({"message": "RequiredParams", "status": "403"}); return
    }; let hability = habilitys.new(req.body["name"], req.body)
    res.status(200)
    .json(hability.hability_data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}
export function editHability(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let habilitys = guild.get_habilitys()
    let hability = habilitys.get(req.params.key)
    if (hability == null) {
      res.status(404)
      .json({"message": "HabilityNotExists", "status": "404"}); return
    } else if (req.body == undefined) {
      res.status(200)
      .json(hability.hability_data); return
    }; hability.edit(req.body); habilitys.save()
    res.status(200)
    .json(hability.hability_data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}