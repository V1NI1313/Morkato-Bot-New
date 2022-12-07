const bodyParser = require("body-parser")
const express = require("express")
const app = express()
/* Guild data functions */
const {
  getGuild,
  newGuild,
  editGuild,
  deleteGuild
} = require("./src/Guild")
/* Hability functions */
const { 
  getAllHabilitys,
  getHability,
  newHability,
  editHability,
  deleteHability
} = require("./src/Hability")
/* Family functions */
const {
  getAllFamilys,
  getFamily,
  newFamily,
  editFamily,
  deleteFamily
} = require("./src/Family")
/* User functions */
const {
  getAllUsers,
  getUser,
  newUser,
  editUser,
  deleteUser
} = require("./src/Users")
/* Player functions */
const {
  getAllPlayers,
  getPlayer,
  newPlayer,
  editPlayer,
  deletePlayer
} = require("./src/Players")

app.use(bodyParser.json())

app.get("/desktop/Guilds/:id", getGuild)
app.post("/desktop/Guilds/:id", newGuild)
app.patch("/desktop/Guilds/:id", (req, res) => {})
app.delete("/desktop/Guilds/:id", (req, res) => {})

app.get("/desktop/Guilds/:id/Hability", getAllHabilitys)
app.get("/desktop/Guilds/:id/Hability/:key", getHability)
app.post("/desktop/Guilds/:id/Hability", newHability)
app.patch("/desktop/Guilds/:id/Hability/:key", editHability)
app.delete("/desktop/Guilds/:id/Hability/:key", (req, res) => {})

app.get("/desktop/Guilds/:id/Family", getAllFamilys)
app.get("/desktop/Guilds/:id/Family/:key", getFamily)
app.post("/desktop/Guilds/:id/Family", newFamily)
app.patch("/desktop/Guilds/:id/Family", (req, res) => {})
app.delete("/desktop/Guilds/:id/Family", (req, res) => {})


app.get("/desktop/Guilds/:id/Users", getAllUsers)
app.get("/desktop/Guilds/:id/Users/:key", getUser)
app.post("/desktop/Guilds/:id/Users/:key", newUser)
app.patch("/desktop/Guilds/:id/Users/:key", editUser)
app.delete("/desktop/Guilds/:id/Users/:key", deleteUser)

app.get("/desktop/Guilds/:id/Players", getAllPlayers)
app.get("/desktop/Guilds/:id/Players/:key", (req, res) => {})
app.post("/desktop/Guilds/:id/Players/:key", (req, res) => {})
app.delete("/desktop/Guilds/:id/Players/:key", (req, res) => {})

app.listen(5500, () => console.log("Server running..."))

