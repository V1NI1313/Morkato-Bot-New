import { writeFileSync } from 'fs'
import { getitem } from './utils'
import { Guild } from './Guild'
import { Json } from './types'
import path from 'path'

let drr = path.normalize(path.join(__dirname, '../', '../', "/Json"))

export interface ChoiceInv {
  choice: number,
  inventory: Json
} export interface UserDDO {
  breed: number|null,
  id: string|number,
  rolls: {
    family: ChoiceInv,
    hability: ChoiceInv
  }
} let userData: UserDDO = {
  breed: null,
  id: "1234567890",
  rolls: {
    family: {
      choice: 3,
      inventory: {}
    },
    hability: {
      choice: 5,
      inventory: {}
    }
  }
}

export function fixData(data: Json, user: UserDDO): UserDDO {
  data["breed"] = getitem(data, "breed", user["breed"])
  data["id"] = user["id"]
  if(data["rolls"] !== undefined) {
    if(data["rolls"]["family"] !== undefined) {
      data["rolls"]["family"] = {
        choice: getitem(data["rolls"]["family"], "choice", user["rolls"]["family"]["choice"]),
        inventory: getitem(data["rolls"]["family"], "inventory", user["rolls"]["family"]["inventory"])
      }
    } else {
      data["rolls"]["family"] = user["rolls"]["family"]
    }; if(data["rolls"]["hability"] !== undefined) {
      data["rolls"]["hability"] = {
        choice: getitem(data["rolls"]["hability"], "choice", user["rolls"]["hability"]),
        inventory: getitem(data["rolls"]["hability"], "inventory", user["rolls"]["hability"]["inventory"])
      }
    } else {
      data["rolls"]["hability"] = user["rolls"]["hability"]
    }
  } else {
    data["rolls"] = user["rolls"]
  }; return {
    breed: data["breed"],
    id: data["id"],
    rolls: data["rolls"]
  }
}

export class Users extends Array<User> {
  public guild: Guild;
  constructor(guild: Guild, users: UserDDO[]) {
    let callable = (): User[] => {
      let array: User[] = []; for(let user of users) {
        array.push(new User(user))
      }; return array
    }; super(...callable())
    this.guild = guild
  } public toJson(): UserDDO[] {
    let array: UserDDO[] = []; for(let user of this) {
      array.push(user.data)
    }; return array
  } public get(id: string|number): User|null {
    for(let user of this) {
      if(user.id == id) {return user;}
    }; return null
  } public new(id: string|number): User {
    userData["id"] = id
    userData["rolls"]["family"]["choice"] = this.guild.player["rolls"]["family"]
    userData["rolls"]["hability"]["choice"] = this.guild.player["rolls"]["hability"]
    this.push(new User(userData))
    this.save()
    return this[this.length-1]
  } public save(): void {
    writeFileSync(`${drr}/Users/${this.guild.id}.json`, JSON.stringify(this.toJson(), null, 2), {encoding: 'utf-8'})
  }
}
export class User {
  public data: UserDDO;
  public id: string|number;
  public familys: Json;
  public habilitys: Json;
  constructor(data: UserDDO) {
    this.data = data
    this.id = data["id"]
    this.familys = data["rolls"]["family"]["inventory"]
    this.habilitys = data["rolls"]["hability"]["inventory"]
  } public edit(data: Json) {
    this.data = fixData(data, this.data)
  }
}