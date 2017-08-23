const request = require('request-promise')
const config = _require('lib/config').tmdb

module.exports = function tmdb(route, qs, options) {
  options = options || {}
  options.qs = options.qs || {}
  options.qs.api_key = options.qs.api_key || config.api_key
  options.json = options.json || true
  route = route[0] == '/' ? route.slice(1) : route

  for (let key in qs) qs.hasOwnProperty(key) && (options.qs[key] = qs[key])
  console.log('https://api.themoviedb.org/3/' + route, options)
  return request('https://api.themoviedb.org/3/' + route, options)
}
