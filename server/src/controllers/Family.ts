import { Response, Request } from "express"
import { Guild, byID } from "../../utils/Guild"

export function getAllFamilys(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let familys = guild.get_familys()
    res.status(200)
    .json(familys.toJson())
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}; export function getFamily(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let family = guild.get_familys().get(req.params.key)
    if(family == null) {
      res.status(404)
      .json({"message": "FamilyNotExists", "status": "404"}); return
    } res.status(200)
    .json(family.family_data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}; export function newFamily(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let familys = guild.get_familys()
    if(req.body["name"] == undefined) {
      res.status(403)
      .json({"message": "RequiredParams", "status": "403"}); return
    }; let family = familys.new(req.body["name"], req.body)
    res.status(200)
    .json(family.family_data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}; export function editFamily(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let familys = guild.get_familys()
    let family = familys.get(req.params.key)
    if(family == null) {
      res.status(404)
      .json({"message": "FamilyNotExists", "status": "404"}); return
    } else if(req.body == undefined) {
      res.status(200)
      .json(family.family_data); return
    }; family.edit(req.body)
    familys.save()
    res.status(200)
    .json(family.family_data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}