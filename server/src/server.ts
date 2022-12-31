import { Router, Request, Response } from 'express';
import { pythonObjects } from './utils'
import axios from 'axios';
import express from 'express'
/* Imports utils */
import {
  getGuild,
  newGuild
} from './controllers/Guild'
import { 
  getAllHabilitys,
  getHability,
  newHability,
  editHability
} from './controllers/Habilitys'
import {
  getAllFamilys,
  getFamily,
  newFamily,
  editFamily
} from './controllers/Family'
import {
  getAllUsers,
  getUser,
  newUser,
  editUser
} from './controllers/Users'
import {
  getAllPlayers,
  getPlayer,
  newPlayer
} from './controllers/Players'
const app = express();
const route = Router()

const headers = {
  'authorization': "Bot OTcyMTkzOTEzOTgzMTAzMDU2.Ggiluu.pHTjdOmlXmk8qRye0U1tZZyGMJDmmSAMGfh1Qs"
}

app.use(express.json())
app.use((req, res, next) => {
  let content = `**new Connection \`${req.url.toString()}\`\nMethod \`${req.method}\`\nPayLoad \`${req.body.toString()}}\`**`
  axios.post("https://discordapp.com/api/v6/channels/1058562996747636757/messages", {content: content}, {headers: headers})
  next();
})
app.use(route)

route.get("/desktop/Guilds/:id", getGuild)
route.post("/desktop/Guilds/:id", newGuild)
// route.patch("/desktop/Guilds/:id", (req, res) => {})
// route.delete("/desktop/Guilds/:id", (req, res) => {})

route.get("/desktop/Guilds/:id/Hability", getAllHabilitys)
route.get("/desktop/Guilds/:id/Hability/:key", getHability)
route.post("/desktop/Guilds/:id/Hability", newHability)
route.patch("/desktop/Guilds/:id/Hability/:key", editHability)
// route.delete("/desktop/Guilds/:id/Hability/:key", (req, res) => {})

route.get("/desktop/Guilds/:id/Family", getAllFamilys)
route.get("/desktop/Guilds/:id/Family/:key", getFamily)
route.post("/desktop/Guilds/:id/Family", newFamily)
route.patch("/desktop/Guilds/:id/Family/:key", editFamily)
// route.delete("/desktop/Guilds/:id/Family", (req, res) => {})


route.get("/desktop/Guilds/:id/Users", getAllUsers)
route.get("/desktop/Guilds/:id/Users/:key", getUser)
route.post("/desktop/Guilds/:id/Users/:key", newUser)
route.patch("/desktop/Guilds/:id/Users/:key", editUser)
// route.delete("/desktop/Guilds/:id/Users/:key", deleteUser)

route.get("/desktop/Guilds/:id/Players", getAllPlayers)
route.get("/desktop/Guilds/:id/Players/:key", getPlayer)
route.post("/desktop/Guilds/:id/Players/:key", newPlayer)
// route.delete("/desktop/Guilds/:id/Players/:key", (req, res) => {})

app.listen(5500, () => console.log("Server running..."))