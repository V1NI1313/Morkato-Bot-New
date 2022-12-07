const { request, response } = require("express")
const { get, fixUserData } = require("../functools")
const path = require("path")
const fs = require("fs")

let drr = path.normalize(path.join(__dirname, '../', '../Json'))

function getAllUsers(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Users/${fileName}`, {encoding: "utf-8"})
    let Users = JSON.parse(file.toString())
    res.status(200)
    res.json(Users)
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists"})
  }
}
function getUser(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Users/${fileName}`, {encoding: "utf-8"})
    let Users = JSON.parse(file.toString())
    for(let i of Users) {if (i["id"] == req.params.key) {res.status(200); res.json(i); return;}}
    res.status(404)
    res.json({"message": "UserNotExists", "status": "404"})
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists"})
  }
}
function newUser(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Users/${fileName}`, {encoding: "utf-8"})
    let fileGuild = fs.readFileSync(`${drr}/Guilds/${fileName}`, {encoding: "utf-8"})
    let Guild = JSON.parse(fileGuild.toString())
    let Users = JSON.parse(file.toString())
    for(let o of Users) {if (req.params.id == o["id"]) {res.status(402).json({"message": "UserAlreadyExists"}); return}}
    User["id"] = req.params.key
    User["rolls"]["family"]["choice"] = Guild["player"]["rolls"]["family"]
    User["rolls"]["hability"]["choice"] = Guild["player"]["rolls"]["hability"]
    Users.unshift(User)
    fs.writeFileSync(`${drr}/Users/${fileName}`, JSON.stringify(Users, null, 2), {encoding: "utf-8"})
    res.status(200)
    res.json(User)
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists"})
  }
}
function editUser(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Users/${fileName}`, {encoding: "utf-8"})
    let Users = JSON.parse(file.toString())
    let response = req.body
    for(let i=0; i<Users.length; i++) {
      if (Users[i]["id"] == req.params.key) {
        Users[i] = fixUserData(response, Users[i])
        fs.writeFileSync(`${drr}/Users/${fileName}`, JSON.stringify(Users, null, 2), {encoding: "utf-8"})
        res.status(200)
        res.json(Users[i])
        return
      }
    }
    res.status(404)
    res.json({"message": "UserNotExists", "status": "404"})
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists"})
  }
}
function deleteUser(req=request, res=response) {
  try {
    let fileName = `${req.params.id}.json`
    let file = fs.readFileSync(`${drr}/Users/${fileName}`, {encoding: "utf-8"})
    let Users = JSON.parse(file.toString())
    for(let i=0; i<Users.length; i++) {
      if (Users[i]["id"] == req.params.key) {
        Users.splice(i, 1)
        fs.writeFileSync(`${drr}/Users/${fileName}`, JSON.stringify(Users, null, 2), {encoding: "utf-8"})
        res.status(200)
        res.json({"message": "UserDeleted", "status": 200})
        return
      }
    }
    res.status(404)
    res.json({"message": "UserNotExists", "status": "404"})
  } catch {
    res.status(404)
    res.json({"message": "GuildNotExists"})
  }
}

let User = {
  "breed": null,
  "id": null,
  "rolls": {
    "family": {"choice": 3, "inventory": {}},
    "hability": {"choice": 3, "inventory": {}}
  }
}

module.exports = {
  getAllUsers,
  getUser,
  newUser,
  editUser,
  deleteUser
}
