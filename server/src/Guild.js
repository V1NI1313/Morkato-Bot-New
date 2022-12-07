const { request, response } = require("express")
const { get } = require("../functools")
const path = require("path")
const fs = require("fs")

let drr = path.normalize(path.join(__dirname, '../', '../Json'))

function getGuild(req=request, res=response) {
  try {
    let file = fs.readFileSync(`${drr}/Guilds/${req.params.id}.json`, {encoding: "utf-8"})
    let json = JSON.parse(file.toString())
    res.status(200)
    res.json(json)
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists", "status": "404"})
  }
}
function newGuild(req=request, res=response) {
  try {
    fs.readFileSync(`${drr}/Guilds/${req.params.id}.json`, {encoding: "utf-8"})
    res.status(402)
    res.json({"message": "GuildAlreadyExists", "status": "402"})
  } catch {
    let response = req.body
    Guild["roles"]["human"] = response.human
    Guild["roles"]["oni"] = response.oni
    Guild["roles"]["hybrid"] = response.hybrid
    Guild["roles"]["separator"] = response.separator
    let fileName = `${req.params.id}.json`
    fs.writeFileSync(`${drr}/Guilds/${fileName}`, JSON.stringify(Guild, null, 2), {encoding: "utf-8"})
    fs.writeFileSync(`${drr}/Family/${fileName}`, "[]", {encoding: "utf-8"})
    fs.writeFileSync(`${drr}/Users/${fileName}`, "[]", {encoding: "utf-8"})
    fs.writeFileSync(`${drr}/Players/${fileName}`, "[]", {encoding: "utf-8"})
    fs.writeFileSync(`${drr}/Hability/${fileName}`, "[]", {encoding: "utf-8"})
    res.status(200)
    res.json(Guild)
  }
}
function editGuild(req=request, res=response) {}
function deleteGuild(req=request, res=response) {}
let Guild = {
  "roles": {
    /*
    Roles config data

    - human: Role human
    - Oni: Role oni
    - hybrid: Role hybrid

    >>> Separator roles added in command /register before register.
    */
    "human": null,
    "oni": null,
    "hybrid": null,
    "separator": []
  },
  "player": {
    /*
    Player config data

    - NickFormat: PlayerFormat nick
    - DefaultStatus: Initial status before creation player register
    */
    "PlayerFormat": "{nick} {year} |\u2764\ufe0f{life}|{err}{stamina}",
    "defaultStatus": {
      "human": {
        "life": 3000,
        "stamina": 3000
      },
      "oni": {
        "life": 6000,
        "stamina": 6000
      },
      "hybrid": {
        "life": 3000,
        "stamina": 6000
      }
    },
    "rolls": {
      /*
      Rolls config data

      - Rolls: Initial roles after creation register player
      */
      "family": 3,
      "hability": 3
    }
  },
  "config": {
    "playerBreed": 0
      /* 
      Verification of player breed in random or by choice

      0 - Choice
      1 - Random
      */
  }
}

module.exports = {
  getGuild,
  newGuild,
  editGuild,
  deleteGuild
}
