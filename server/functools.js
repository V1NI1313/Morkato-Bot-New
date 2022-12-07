function get(_object, key, _default=null)
{
  let obj = _object[key]
  if (obj !== undefined) {return obj}
  return _default
}
function fixHabilityData(data, hability) {
  data['name'] = get(data, "name", hability["name"])
  data['id'] = hability["id"]
  data['role'] = get(data, "role", hability["role"])
  data['roles'] = get(data, "roles", hability["roles"])
  data['rarity'] = get(data, "rarity", hability["rarity"])
  data["require"] = get(data, "require", hability["require"])
  if (get(data, "embed") !== null) {
    data["embed"]["title"] = get(data["embed"], "title", hability["embed"]["title"])
    data["embed"]["description"] = get(data["embed"], "description", hability["embed"]["description"])
    data["embed"]["url"] = get(data["embed"], "url", hability["embed"]["url"])
  } else {data["embed"] = hability["embed"]}
  return {
    "name": data['name'],
    "id": data["id"],
    "role": data["role"],
    "roles": data["roles"],
    "rarity": data["rarity"],
    "require": data["require"],
    "embed": data["embed"]
  }
}
function fixUserData(data, user) {
  user["breed"] = get(data, "breed", user["breed"])
  if (get(data, "rolls") !== null) {
    if (get(data["rolls"], "family") !== null) {
      user["rolls"]["family"]["choice"] = get(user["rolls"]["family"], "choice", user["rolls"]["family"]["choice"])
      user["rolls"]["family"]["inventory"] = get(user["rolls"]["family"], "inventory", user["rolls"]["family"]["inventory"])
    }
    if (get(data["rolls"], "hability") !== null) {
      user["rolls"]["hability"]["choice"] = get(user["rolls"]["family"], "choice", user["rolls"]["hability"]["choice"])
      user["rolls"]["hability"]["inventory"] = get(user["rolls"]["family"], "inventory", user["rolls"]["hability"]["inventory"])
    }
  }
  return user
}
module.exports = {
  fixHabilityData,
  fixUserData,
  get
}