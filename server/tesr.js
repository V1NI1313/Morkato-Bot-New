// fetch(`https://www.discord.com/api/v6/guilds/1030300817175089203`, {headers: {Authorization: "Bot OTcyMTkzOTEzOTgzMTAzMDU2.GVyvHa.RWzzo2UsGzY4vdCR4NZYIkEc508V7zz1CKlyJg"}}).then(res => {return res.status}).then(data => console.log(data))
const fs = require("fs")
try {fs.readFileSync("./ksks")}
catch (err) {
  console.log(err)
}