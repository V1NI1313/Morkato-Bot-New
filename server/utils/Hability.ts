import { readFileSync, writeFileSync } from 'fs'
import { Json, embed, JsonArray } from './types'
import { getitem } from './utils'
import { Guild } from './Guild'
import path from 'path'

let drr = path.normalize(path.join(__dirname, '../', '../', "/Json"))

interface HabilityDDO {
  [x: string]: any,
  name: string,
  id: string,
  role: string|null,
  roles: string[],
  rarity: number,
  require: number,
  embed: embed
}
let HabilityData: HabilityDDO = {
  name: "NAME",
  id: "0",
  role: null,
  roles: [],
  rarity: 0,
  require: 1,
  embed: {
    title: null,
    description: null,
    url: null
  }
}
function fixData(data: Json, hability: HabilityDDO): HabilityDDO {
  data["name"] = getitem(data, "name", hability["name"])
  data["id"] = hability["id"]
  data["role"] = getitem(data, "role", hability["role"])
  data["roles"] = getitem(data, "roles", hability["roles"])
  data["rarity"] = getitem(data, "rarity", hability["rarity"])
  data["require"] = getitem(data, "require", hability["require"])
  if (data["embed"] !== null) {
    data["embed"] = {
      title: getitem(data["embed"], "title", hability["embed"]["title"]),
      description: getitem(data["embed"], "description", hability["embed"]["description"]),
      url: getitem(data["embed"], "url", hability["embed"]["url"])
    }
  } else {
    data["embed"] = hability["embed"]
  }; return {
    name: data["name"],
    id: data["id"],
    role: data["role"],
    roles: data["roles"],
    rarity: data["rarity"],
    require: data["require"],
    embed: data["embed"]
  }
}
export class Habilitys extends Array<Hability> {
  public guild: Guild;
  constructor(guild: Guild, all: HabilityDDO[]) {
    let callable = () => {
      let _all = []
      for(let elem of all) {
        _all.push(new Hability(elem))
      }; return _all
    }; super(...callable())
    this.guild = guild
  }
  public toJson(): HabilityDDO[] {
    let callable = (habilitys: Hability[]) => {let _all=[]; for(let hability of habilitys) {_all.push(hability.hability_data)}; return _all}
    return callable(this)
  }
  public get(id: string|number): Hability|null {
    for(let hability of this) {
      if (hability.id == id) {return hability;}
    }; return null
  }
  public getIndex(id: string|number): number|null {
    for(let i=0;i<this.length;i++) {
      if (this[i].id == id) {return i}
    }; return null
  }
  public new(name: string, opts: Json): Hability {
    opts["name"] = name; HabilityData["id"] = Math.floor(Math.random() * 100000000000000000).toString()
    let data = fixData(opts, HabilityData); this.push(new Hability(data))
    this.save()
    return this[this.length-1]
  }
  public save(): void {
    let callable = (): HabilityDDO[] => {
      let all = []; for(let hability of this) {
        all.push(hability.hability_data)
      } return all
    }; writeFileSync(`${drr}/Hability/${this.guild.id}.json`, JSON.stringify(callable(), null, 2), {encoding: 'utf-8'})
  }
}
interface edit {
  name?: string|null,
  role?: string|null,
  roles?: string[]|null,
  rarity?: number|null,
  require?: number|null,
  embed?: Json|null
}
class Hability {
  public hability_data: HabilityDDO;
  public id: number|string;
  constructor(hability: HabilityDDO) {
    this.id = hability["id"]
    this.hability_data = hability
  }
  public edit(hability: edit): Hability {
    this.hability_data = fixData(hability, this.hability_data)
    return this
  }
}