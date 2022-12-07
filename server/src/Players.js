const { request, response } = require("express")
const { get } = require("../functools")
const path = require("path")
const fs = require("fs")

let drr = path.normalize(path.join(__dirname, '../', '../Json'))

function getAllPlayers(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Players/${fileName}`, {encoding: "utf-8"})
    let Players = JSON.parse(file.toString())
    res.status(200)
    res.json(Players)
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists"})
  }
}
function getPlayer(req=request, res=response) {}
function newPlayer(req=request, res=response) {}
function editPlayer(req=request, res=response) {}
function deletePlayer(req=request, res=response) {}

let Player = {
  "name": null, /* String */
  "nick": null, /* String */
  "age": null, /* Int */
  "id": null, /* Int */
  "history": null, /* String | null */
  "xp": 0, /* Int */
  "level": 1, /* Int */
  "lvMin": 100, /* Int */
  "life": null, /* Int */
  "stamina": null, /* Int */
  "force": null, /* Float */
  "resistance": null, /* Float */
  "historic": [], /* List | Array obejct */
  "inventory": [], /* List | Arrau boject */
  "settings": {} /* Object<String, Boolean> */
}

module.exports = {
  getAllPlayers,
  getPlayer,
  newPlayer,
  editPlayer,
  deletePlayer
}