const express = require('express');
const cors = require('cors'); 
const serverless = require('serverless-http');
const app = express();

app.use(cors());

const port = process.env.PORT || 3005;
const apidata = require('../data/match.js');

app.get('/', (req, res) => {
    res.send(apidata);
});

app.listen(port, (req, res) => {
    console.log("server started");
});

app.use('/.netlify/funtions/api', express.Router)
module.exports.handler = serverless(app);