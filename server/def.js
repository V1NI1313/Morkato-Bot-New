function get(_object, key, _default=null)
{
    let obj = _object[key]
    if (obj !== undefined) {return obj}
    return _default
}
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
  Guild,
  get
}