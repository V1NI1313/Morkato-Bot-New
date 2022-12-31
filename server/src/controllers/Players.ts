import { Response, Request } from "express"
import { Guild, byID } from "../../utils/Guild"

export function getAllPlayers(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let users = guild.get_users()
    let players = guild.get_players(users)
    res.status(200)
    .json(players.toJsonUnion())
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}
export function getPlayer(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let users = guild.get_users()
    let players =guild.get_players(users)
    let player = players.get(req.params.key)
    if(player == null) {
      res.status(404)
      .json({"message": "PlayerNotExists", "status": "404"}); return
    }; res.status(200)
    .json({...player.user.data, ...player.data})
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}
export function newPlayer(req: Request, res: Response) {
  let guild: Guild; try {
    guild = byID(req.params.id)
    let users = guild.get_users()
    let players = guild.get_players(users)
    let user = users.get(req.params.key)
    if(user == null) {
      res.status(404)
      .json({"message": "UserNotFound", "status": "404"}); return
    }; if(!(players.get(user.id) == null)) {
      res.status(403)
      .json({"message": "PlayerAlreadyExists", "status": "403"}); return
    }; let body = req.body
    if(body["name"] == undefined || body["age"] == undefined || body["family"] == undefined) {
      res.status(403)
      .json({"message": "RequiredParams", "status": "403"}); return
    }; try {
      let player = players.new(user, body["name"], body["age"], body["nick"], body["family"])
      res.status(200)
      .json({...player.user.data, ...player.data})
    } catch {
      res.status(403)
      .json({"message": "NotUsingFamily", "status": "403"})
    }
  } catch {
    res.status(404)
    .json({"message": "GuildNotExists", "status": "404"})
  }
}
// export function getAllPlayers(req: Request, res: Response) {
//   let guild: Guild; try {
//     guild = byID(req.params.id)
//     let users = guild.get_users()
//     let players = guild.get_players(users)
//     let callable = (): PlayerUnion[] => {
//       let callable = (id: string|number): User => {
//         for(let user of users) {
//           if(user.id == id) {return user}
//         }; return users[0]
//       }
//       let array: PlayerUnion[] = []; for(let player of players) {
//         array.push({...callable(player.id).data, ...player.data})
//        }; return array
//     }
//     res.status(200)
//     .json(callable())
//   } catch {}
// }