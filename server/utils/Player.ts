import { User, Users, UserDDO, ChoiceInv, fixData as fixUserData } from './User'
import { writeFileSync } from 'fs'
import { getitem } from './utils'
import { Guild } from './Guild'
import { Json } from './types'
import path from 'path'

let drr = path.normalize(path.join(__dirname, '../', '../', "/Json"))

export interface PlayerDDO {
  name: string,
  nick: string|null,
  age: number,
  id: string|number,
  history: string|null,
  family: string,
  xp: number,
  level: number,
  lvMin: number,
  life: number,
  stamina: number,
  force: number,
  resistance: number,
  historic: [],
  inventory: [],
  settings: {}
}
interface _UserDDO {
  breed: number|null,
  rolls: {
    family: ChoiceInv,
    hability: ChoiceInv
  }
}
interface PlayerUnion extends _UserDDO, PlayerDDO {}

function fixData(data: Json, player: PlayerDDO): PlayerDDO {
  data["name"] = getitem(data, "name", player["name"])
  data["nick"] = getitem(data, "nick", player["nick"])
  data["age"] = getitem(data, "age", player["age"])
  data["id"] = player["id"]
  data["history"] = getitem(data, "history", player["history"])
  data["family"] = getitem(data, "family", player["family"])
  data["xp"] = getitem(data, "xp", player["xp"])
  data["level"] = getitem(data, "level", player["level"])
  data["lvMin"] = getitem(data, "lvMin", player["lvMin"])
  data["life"] = getitem(data, "life", player["life"])
  data["stamina"] = getitem(data, "stamina", player["stamina"])
  data["force"] = getitem(data, "force", player["force"])
  data["resistance"] = getitem(data, "resistance", player["resistance"])
  data["historic"] = getitem(data, "historic", player["historic"])
  data["inventory"] = getitem(data, "inventory", player["inventory"])
  data["settings"] = getitem(data, "settings", player["settings"])
  return {
    name: data["name"],
    nick: data["nick"],
    age: data["age"],
    id: data["id"],
    history: data["history"],
    family: data["family"],
    xp: data["xp"],
    level: data["level"],
    lvMin: data["lvMin"],
    life: data["life"],
    stamina: data["stamina"],
    force: data["force"],
    resistance: data["resistance"],
    historic: data["historic"],
    inventory: data["inventory"],
    settings: data["settings"]
  }
}; let PlayerData: PlayerDDO = {
  name: "NAME",
  nick: null,
  age: 21,
  id: "1234567890",
  history: null,
  family: "1234567890",
  xp: 1,
  level: 1,
  lvMin: 100,
  life: 3000,
  stamina: 3000,
  force: 0.5,
  resistance: 1,
  historic: [],
  inventory: [],
  settings: {}
}

class UserNotRequisits extends Error {
  constructor(id: string|number) {
    super(`User by id ${id} not requisits!`)
  }
}
export class Players extends Array<Player> {
  public guild: Guild;
  constructor(guild: Guild, users: Users, data: PlayerDDO[]) {
    let callable = (): Player[] => {
      let callable = (user: User): PlayerDDO|null => {
        for(let player of data) {
          if(player["id"] == user.id) {return player;}
        }; return null
      }; let array: Player[] = []; for(let user of users) {
        let player = callable(user)
        if(player==null) {
          continue;
        }; array.push(new Player(user, player))
      }; return array
    }; super(...callable())
    this.guild = guild
  } public toJson(): PlayerDDO[] {
    let callable = () => {
      let array: PlayerDDO[] = []; for(let player of this) {
        array.push(player.data)
      }; return array
    }; return callable()
  } public toJsonUnion(): PlayerUnion[] {
    let callable = () => {
      let array: PlayerUnion[] = []; for(let player of this) {
        array.push({...player.user.data, ...player.data})
      }; return array
    }; return callable()
  } public get(id: string|number): Player|null {
    for(let player of this) {
      if(player.id == id) {
        return player
      }
    }; return null
  } public new(
    user: User,
    name: string,
    age: number,
    nick: string|null=null,
    family: string
  ): Player {
    if(nick == undefined) nick = null
  let callable = (): PlayerDDO => {
    let inList = (iter: any[], item: any) => {
      for(let _item of iter) {
        if(_item == item) {return true}
      }; return false
    }; if(!(inList(Object.keys(user.familys), family))) {
      throw new UserNotRequisits(user.id)
    }; PlayerData["family"] = family
    PlayerData["id"] = user.id
    PlayerData["name"] = name
    PlayerData["nick"] = nick
    PlayerData["age"] = age
    return PlayerData
  }; this.push(new Player(user, callable()))
    writeFileSync(`${drr}/Players/${this.guild.id}.json`, JSON.stringify(this.toJson(), null, 2), {encoding: 'utf-8'})
    return this[this.length-1]
  }
}
class Player {
  public data: PlayerDDO;
  public id: string|number;
  public user: User;
  constructor(user: User, data: PlayerDDO) {
    this.data = data
    this.id = data["id"]
    this.user = user
  } public edit(data: Json) {
    
  }
}