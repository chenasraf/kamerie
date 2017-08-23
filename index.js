// global require function: _require(module)
require('./req')('_require')
require('dotenv').config()
const express = require('express')
const app = express()
const apiRouter = express.Router()
const tmdb = _require('lib/tmdb')
// const { graphql, buildSchema } = require('graphql')
//
// const movies = buildSchema(`
//   type Movie {
//     name: String
//   }
// `)

apiRouter.get('/search/:query', (req, res) => {
  console.log('GET /search,', req.params.query)
  let query = req.params.query
  let year
  const YEAR_REGEX =  /(\d{2}){2}/i
  if (YEAR_REGEX.test(query)) {
    let matches = YEAR_REGEX.exec(query)
    year = matches[0]
    let yearIdx = query.indexOf(year)
    query = query.slice(0, yearIdx) + query.slice(yearIdx + year.length)
  }
  tmdb('/search/movie/', {query, year}).then(response => {
    res.json(response.results)
  })
})

app.use('/api', apiRouter)
app.use((err, req, res, next) => {
  if (err) {
    console.error(err)
    return res.status(500).json(err)
  }
})

app.listen(3000, function() {
  console.log('Listening on port 3000')
})
