const { get, fixHabilityData } = require("../functools")
const { request, response } = require("express")
const path = require("path")
const fs = require("fs")

let drr = path.normalize(path.join(__dirname, '../', '../Json'))

function getAllHabilitys(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Hability/${fileName}`)
    let Habilitys = JSON.parse(file.toString())
    res.status(200)
    res.json(Habilitys)
  } catch {
    res.status(402)
    res.json({"message": "GuildNotExists", "status": "402"})
  }
}
function getHability(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Hability/${fileName}`)
    let Habilitys = JSON.parse(file.toString())
    let key = req.params.key
    for(let i of Habilitys) {
      if (key == i["info"]["id"]) {
        res.status(200)
        res.json(i)
        return
      }
    }
    res.status(404)
    res.json({"message": "HabilityNotExists", "status": "404"})
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists", "status": "404"})
  }
}
function newHability(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Hability/${fileName}`)
    let Habilitys = JSON.parse(file.toString())
    let response = req.body
    for(let i of Habilitys) {
      if (get(response, "role") == i["role"]) {
        res.status(404)
        res.json({"message": "HabilityAlreadyExists", "status": "404"})
        return
      }
    }
    Hability["name"] = response["name"]
    Hability["id"] = Math.floor(Math.random() * 100000000000000).toString()
    Hability["role"] = get(response, "role")
    Habilitys.push(Hability)
    fs.writeFileSync(`${drr}/Hability/${fileName}`, JSON.stringify(Habilitys, null, 2), {encoding: "utf-8"})
    res.status(200)
    res.json(Hability)
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists", "status": "404"})
  }
}
function editHability(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Hability/${fileName}`)
    let Habilitys = JSON.parse(file.toString())
    let response = req.body
    for(let i=0; i < Habilitys.length; i++) {
      if (Habilitys[i]["id"] == req.params.key) {
        Habilitys[i] = fixHabilityData(response, Habilitys[i])
        fs.writeFileSync(`${drr}/Hability/${fileName}`, JSON.stringify(Habilitys, null, 2), {encoding: "utf-8"})
        res.status(200)
        res.json(Habilitys[i])
        return
      }
    }
    res.status(404)
    res.json({"message": "HabilityNotExists", "status": "404"})
  } catch {
    res.status(402)
    res.json({"message": "GuildNotExists", "status": "402"})
  }
}
function deleteHability(req=request, res=response) {}

let Hability = {
  "name": null, /* String */
  "id": 99999999999, /* Int**12 */
  "role": null, /* List discord role id */
  "roles": [], /* Require discord roles id */
  "rarity": 0,
  /*
  Rarity types

  0 - Commom
  1 - Rare
  2 - Epic
  3 - Legendary
  */
  "require": 0, /* Int */
  "embed": {
    "title": null,
    "description": null,
    "url": null
  }
}

module.exports = {
  getAllHabilitys,
  getHability,
  newHability,
  editHability,
  deleteHability
}