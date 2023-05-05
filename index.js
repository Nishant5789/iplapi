const express = require('express');
const cors = require('cors'); 
const app = express();

app.use(cors());

const port = process.env.PORT || 3005;
const apidata = require('./data/match.js');

app.get('/', (req, res) => {
    res.send(apidata);
});

app.listen(port, (req, res) => {
    console.log("server started");
});

