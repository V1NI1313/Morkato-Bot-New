import { Json, JsonArray, embed } from "./types"
import { writeFileSync } from 'fs'
import { Guild } from "./Guild"
import { getitem } from "./utils"
import path from 'path'

let drr = path.normalize(path.join(__dirname, '../', '../', "/Json"))

interface FamilyDDO {
  name: string,
  id: string|number,
  role: string|number|null,
  roles: string[],
  habilitys: string[],
  rarity: number,
  require: number,
  limit: number|null,
  embed: embed,
  message: {
    content: string|null,
    url: string|null
  }
}
let FamilyData: FamilyDDO = {
  name: "NAME",
  id: "5500550",
  role: null,
  roles: [],
  habilitys: [],
  rarity: 0,
  require: 1,
  limit: null,
  embed: {
    title: null,
    description: null,
    url: null
  },
  message: {
    content: null,
    url: null
  }
}

function fixData(data: Json, family: FamilyDDO): FamilyDDO {
  data["name"] = getitem(data, "name", family["name"])
  data["id"] = family["id"]
  data["role"] = getitem(data, "role", family["role"])
  data["roles"] = getitem(data, "roles", family["roles"])
  data["habilitys"] = getitem(data, "habilitys", family["habilitys"])
  data["rarity"] = getitem(data, "rarity", family["rarity"])
  data["require"] = getitem(data, "require", family["require"])
  data["limit"] = getitem(data, "limit", family["limit"])
  if(data["embed"] !== undefined) {
    data["embed"] = {
      title: getitem(data["embed"], "title", family["embed"]["title"]),
      description: getitem(data["embed"], "description", family["embed"]["description"]),
      url: getitem(data["embed"], "url", family["embed"]["url"])
    }
  } else {data["embed"] = family["embed"]}
  if(data["message"] !== undefined) {
    data["message"] = {
      content: getitem(data["message"], "content", family["message"]["content"]),
      url: getitem(data["message"], "url", family["message"]["url"])
    } 
  } else {data["message"] = family["message"]}; return {
    name: data["name"],
    id: data["id"],
    role: data["role"],
    roles: data["roles"],
    habilitys: data["habilitys"],
    rarity: data["rarity"],
    require: data["require"],
    limit: data["limit"],
    embed: data["embed"],
    message: data["message"]
  }
}

export class Familys extends Array<Family> {
  public guild: Guild
  constructor(guild: Guild, all: FamilyDDO[]) {
    let callable = () => {
      let array: Family[] = []
      for(let elem of all) {
        array.push(new Family(elem))
      }; return array
    }; super(...callable())
    this.guild = guild
  }
  public toJson(): FamilyDDO[] {
    let callable = (): FamilyDDO[] => {
      let array: FamilyDDO[] = []
      for(let family of this) {
        array.push(family.family_data)
      }; return array
    }; return callable()
  }
  public get(id: string): Family|null {
    for(let family of this) {
      if(family.id == id) {return family;}
    }; return null
  }
  public new(name: string, opts: Json): Family {
    opts["name"] = name
    FamilyData["id"] = Math.floor(Math.random() * 100000000000000000).toString()
    let data = fixData(opts, FamilyData)
    this.push(new Family(data))
    this.save()
    return this[this.length-1]
  }
  public save(): void {
    let fileName = `${drr}/Family/${this.guild.id}.json`
    let array: FamilyDDO[] = this.toJson()
    writeFileSync(fileName, JSON.stringify(array, null, 2), {encoding: 'utf-8'})
  }
}
export class Family {
  public id: string|number;
  public family_data: FamilyDDO;
  constructor(data: FamilyDDO) {
    this.family_data = data
    this.id = data["id"]
  }
  public edit(family: Json): Family {
    this.family_data = fixData(family, this.family_data)
    return this
  }
}