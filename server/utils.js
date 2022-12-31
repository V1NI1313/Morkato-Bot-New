class dictionary {
  /**
   * 
   * @param {Object} obj 
   */
  constructor(obj) {
    this.obj = obj
    console.log(typeof(obj))
  }
  /**
   * 
   * @param {String} key 
   * @param {String | Number | Boolean | null} value 
   */
  get(key, value=null) {
    return this.obj[key]
  }
}

module.exports = {
  dictionary
}