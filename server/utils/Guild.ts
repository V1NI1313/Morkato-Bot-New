import { readFileSync, writeFileSync } from 'fs'
import { Json, JsonArray } from './types'
import { getitem } from '../src/utils'
import { Habilitys } from './Hability'
import { Familys } from './Family'
import { Players } from './Player'
import { Users } from './User'
import path from 'path'

let drr = path.normalize(path.join(__dirname, '../', '../', "/Json"))

function fixData(data: Json|any, guild: GuildDDO): GuildDDO {
  if (data["roles"] !== undefined) {
    data["roles"] = {
      human: getitem(data["roles"], "human", guild["roles"]["human"]),
      oni: getitem(data["roles"], "oni", guild["roles"]["oni"]),
      hybrid: getitem(data["roles"], "hybrid", guild["roles"]["hybrid"])
    }
  } else {data["roles"] = guild["roles"];}
  if (data["player"] !== undefined) {
    data["player"] = {
      PlayerFormat: getitem(data["player"], "PlayerFormat", guild["player"]["PlayerFormat"]),
      defaultStatus: guild["player"]["defaultStatus"],
      rolls: guild["player"]["rolls"]
    }
  } else {data["player"] = guild["player"]} 
  return {
    roles: data["roles"],
    player: data["player"],
    settings: guild["settings"]
  }
}

interface GuildRoles {
  human: string | number | null,
  oni: string | number | null,
  hybrid: string | number | null
}
interface GuildPlayerDefaultStatusOPP {
  life: number,
  stamina: number
}
interface GuildPlayerDefaultRolls {
  family: number,
  hability: number
}
interface GuildPlayerDefaultStatus {
  human: GuildPlayerDefaultStatusOPP,
  oni: GuildPlayerDefaultStatusOPP,
  hybrid: GuildPlayerDefaultStatusOPP
}
interface GuildPlayer {
  PlayerFormat: string,
  defaultStatus: GuildPlayerDefaultStatus,
  rolls: GuildPlayerDefaultRolls
}
interface GuildSettings {
  autoplayerBreed: number
}
interface GuildDDO {
  roles: GuildRoles
  player: GuildPlayer
  settings: GuildSettings
}

export class GuildNotExists extends Error {constructor(id: string|number) {super(`Guild id ${id} not exists!`)};}
export class Guild {
  public id: string|number;
  public roles: GuildRoles;
  public player: GuildPlayer;
  public settings: GuildSettings;
  constructor(id: string|number, data: GuildDDO) {
    this.id = id
    this.roles = data['roles']
    this.player = data['player']
    this.settings = data['settings']
  }
  public parse(): GuildDDO {return {roles: this.roles, player: this.player, settings: this.settings};}
  public save(): Guild {
    let fileName: string = `${drr}/Guilds/${this.id}.json`
    let save: GuildDDO = this.parse();
    writeFileSync(fileName, JSON.stringify(save, null, 2), {encoding: 'utf-8'})
    return new Guild(this.id, save)
  }
  public get_habilitys(): Habilitys {
    let fileName = `${drr}/Hability/${this.id}.json`; try {
      let file = readFileSync(fileName, {encoding: 'utf-8'}).toString()
      return new Habilitys(this, JSON.parse(file))
    } catch {
      writeFileSync(fileName, "[]", {encoding: 'utf-8'})
      return new Habilitys(this, [])
    }
  }
  public get_familys(): Familys {
    let fileName = `${drr}/Family/${this.id}.json`; try {
      let file = readFileSync(fileName, {encoding: 'utf-8'}).toString()
      return new Familys(this, JSON.parse(file))
    } catch {
      writeFileSync(fileName, "[]", {encoding: 'utf-8'})
      return new Familys(this, [])
    }
  }
  public get_users(): Users {
    let fileName = `${drr}/Users/${this.id}.json`; try {
      let file = readFileSync(fileName, {encoding: 'utf-8'}).toString()
      return new Users(this, JSON.parse(file))
    } catch {
      writeFileSync(fileName, "[]", {encoding: 'utf-8'})
      return new Users(this, [])
    }
  }
  public get_players(users: Users): Players {
    let fileName = `${drr}/Players/${this.id}.json`; try {
      let file = readFileSync(fileName, {encoding: 'utf-8'}).toString()
      return new Players(this, users, JSON.parse(file))
    } catch {
      writeFileSync(fileName, "[]", {encoding: 'utf-8'})
      return new Players(this, users, [])
    }
  }
}
export function byID(id: string|number): Guild {
  try {
    let fileName: string = `${drr}/Guilds/${id}.json`
    let file: string = readFileSync(fileName, {encoding: 'utf-8'}).toString()
    let GuildOptions: GuildDDO = JSON.parse(file)
    return new Guild(id, GuildOptions)
  } catch {
    throw new GuildNotExists(id)
  }
}
let guildData: GuildDDO = {
  roles: {
    human: null,
    oni: null,
    hybrid: null
  },
  player: {
    PlayerFormat: "{nick} {year} |❤️{life}|{err}{stamina}",
    defaultStatus: {
      human: {
        life: 3000,
        stamina: 3000
      },
      oni: {
        life: 6000,
        stamina: 6000
      },
      hybrid: {
        life: 6000,
        stamina: 3000
      }
    },
    rolls: {
      family: 3,
      hability: 5
    }
  },
  settings: {
    autoplayerBreed: 0
  }
}
export function New_Guild(id: string|number, data: Json|any): Guild {
  let datafix: GuildDDO = fixData(data, guildData)
  let fileName: string = `${drr}/Guilds/${id}.json`
  writeFileSync(fileName, JSON.stringify(datafix), {encoding: 'utf-8'})
  return new Guild(id, datafix)
}