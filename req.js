const path = require('path')

module.exports = function (fn) {
  global[fn] = function appRequire(name) {
    return require(path.resolve(__dirname, name))
  }
}
