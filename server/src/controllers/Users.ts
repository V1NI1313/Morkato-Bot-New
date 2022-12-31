import { Response, Request } from 'express'
import { Guild, byID } from "../../utils/Guild"

export function getAllUsers(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let users = guild.get_users()
    res.status(200)
    .json(users.toJson())
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
} export function getUser(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let users = guild.get_users()
    let user = users.get(req.params.key)
    if(user == null) {
      res.status(404)
      .json({"message": "UserNotExists", "status": "404"}); return
    }; res.status(200)
    .json(user.data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
} export function newUser(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let users = guild.get_users()
    let user = users.get(req.params.key)
    if(user !== null) {
      res.status(403)
      .json({"message": "UserAlreadyExists", "status": "404"}); return
    }; user = users.new(req.params.key)
    res.status(200)
    .json(user.data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
} export function editUser(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let users = guild.get_users()
    let user = users.get(req.params.key)
    if(user == null) {
      res.status(404)
      .json({"message": "UserNotExists", "status": "404"}); return
    } else if(req.body == undefined) {
      res.status(200)
      .json(user.data); return
    }; user.edit(req.body)
    users.save()
    res.status(200)
    .json(user.data)
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}