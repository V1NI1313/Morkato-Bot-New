const { request, response } = require("express")
const { get } = require("../functools")
const path = require("path")
const fs = require("fs")

let drr = path.normalize(path.join(__dirname, '../', '../Json'))

function getAllFamilys(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Family/${fileName}`)
    let Familys = JSON.parse(file.toString())
    res.status(200)
    res.json(Familys)
  } catch {
    res.status(402)
    res.json({"message": "GuildNotExists", "status": "402"})
  }
}
function getFamily(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Family/${fileName}`)
    let Familys = JSON.parse(file.toString())
    let key = req.params.key
    for(let i of Familys) {
      if (key == i["id"]) {
        res.status(200)
        res.json(i)
        return
      }
    }
    res.status(402)
    res.json({"message": "FamilyNotExists", "status": "402"})
  } catch {
    res.status(402)
    res.json({"message": "GuildNotExists", "status": "402"})
  }
}
function newFamily(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Family/${fileName}`)
    let Familys = JSON.parse(file.toString())
    let response = req.body
    for(let i of Familys) {
      if (response["name"] == i["name"]) {
        res.status(402)
        res.json({"message": "FamilyAlreadyExists", "status": "402"})
        return
      }
    }
    Family["info"]["name"] = response["name"]
    Family["info"]["id"] = Math.floor(Math.random() * 100000000000000).toString()
    Family["info"]["role"] = get(response, "role")
    Familys.unshift(Family)
    fs.writeFileSync(`${drr}/Family/${fileName}`, JSON.stringify(Familys, null, 2))
    res.status(200)
    res.json(Family)
  } catch {
    res.status(402)
    res.json({"message": "GuildNotExists", "status": "402"})
  }
}
function editFamily(req=request, res=response) {}
function deleteFamily(req=request, res=response) {}

let Family = {
  "info": {
    "name": null,
    "id": null,
    "role": null,
    "habilitys": [],
    "roles": [],
    /*
    Rarity types:

    0 - Commom
    1 - Rare
    2 - Epic
    3 - Legendary
    */
    "rarity": 0,
    "require": 1,
    "limit": null
  },
  "content": {
    "title": null,
    "description": null
  },
  "message": {
    "content": null,
    /*
    File decoder:

    0 - Binary
    1 - String
    3 - Url
    */
    "fileDecoder": 0,
    "file": null
  }
}

module.exports = {
  getAllFamilys,
  getFamily,
  newFamily,
  editFamily,
  deleteFamily
}