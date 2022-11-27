const bodyParser = require("body-parser")
const { Guild, get } = require("./def")
const express = require("express")
const path = require("path")
const fs = require("fs")
const app = express()

let drr = path.join(__dirname, '../Json')
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

app.get("/desktop/Guilds/:id", (req, res) => {
  try {
    let file = fs.readFileSync(`${drr}/Guilds/${req.params.id}.json`)
    let json = JSON.parse(file.toString())
    res.status(200)
    res.json(json)
  } catch {
    res.status(402)
    res.json({"message": "GuildNotExists", "status": "402"})
  }
})
app.post("/desktop/Guilds/:id", (req, res) => {
  try {
    fs.readFileSync(`${drr}/Guilds/${req.params.id}.json`)
    res.status(402)
    res.json({"message": "GuildAlreadyExists", "status": "402"})
  } catch {
    let response = req.body
    Guild["roles"]["human"] = response.human
    Guild["roles"]["oni"] = response.oni
    Guild["roles"]["hybrid"] = response.hybrid
    Guild["roles"]["separator"] = response.separator
    let _Guild = {
      "Family": [],
      "Hability": [],
      "Guild": Guild
    }
    let fileName = `${req.params.id}.json`
    fs.writeFileSync(`${drr}/Guilds/${fileName}`, JSON.stringify(_Guild["Guild"], null, 2))
    fs.writeFileSync(`${drr}/Family/${fileName}`, JSON.stringify(_Guild["Family"], null, 2))
    fs.writeFileSync(`${drr}/Hability/${fileName}`, JSON.stringify(_Guild["Hability"], null, 2))
    res.status(200)
    res.json(_Guild["Guild"])
  }
})
app.patch("/desktop/Guilds/:id", (req, res) => {
  // try {
    let Guild = fs.readFileSync(`${drr}/Guilds/${req.params.id}.json`)
    Guild = JSON.parse(Guild.toString())
    let response = req.body
    if (get(response, "roles") !== null) {
      response["roles"] = {
        "human": get(response["roles"], "human", Guild["roles"]["human"]),
        "oni": get(response["roles"], "oni", Guild["roles"]["oni"]),
        "hybrid": get(response["roles"], "hybrid", Guild["roles"]["hybrid"])
      }
    } else {response["roles"] = Guild["roles"]}
    if (get(response, "player") !== null) {
      response["player"]["PlayerFormat"] = get(response["player"], "PlayerFormat", Guild["player"]["PlayerFormat"])
      if (get(response["player"], "defaultStatus") !== null) {
        response["player"]["defaultStatus"]["human"] = get(response["player"]["defaultStatus"], "human", Guild["player"]["defaultStatus"]["human"])
        response["player"]["defaultStatus"]["oni"] = get(response["player"]["defaultStatus"], "oni", Guild["player"]["defaultStatus"]["oni"])
        response["player"]["defaultStatus"]["hybrid"] = get(response["player"]["defaultStatus"], "hybrid", Guild["player"]["defaultStatus"]["hybrid"])
      } else {response["player"]["defaultStatus"] = Guild["player"]["defaultStatus"]}
      if (get(response["player"], "rolls") !== null) {
        response["player"]["rolls"] = {
          "family": get(response["player"]["rolls"], "family", Guild["player"]["rolls"]["family"]),
          "hability": get(response["player"]["rolls"], "hability", Guild["player"]["rolls"]["hability"])
        }
      } else {response["player"]["rolls"] = Guild["player"]["rolls"]}
    } else {response["player"] = Guild["player"]}
    if (get(response, "get") !== null) {
      response["config"]["playerBreed"] = get(response["config"], "playerBreed", Guild["config"]["playerBreed"])
    }
    let fileName = `${req.params.id}.json`
    fs.writeFileSync(`${drr}/Guilds/${fileName}`, JSON.stringify(response, null, 2))
    res.status(200)
    res.json(response)
    // } catch {
    //   res.status(402)
    //   res.json({"message": "GuildNotExists", "status": "402"})
    // }
})
app.listen(5500, () => console.log("Server running..."))