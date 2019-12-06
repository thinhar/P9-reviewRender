const http = require('http');
const app = require('./app');

const port = process.env.PORT || 80;

const server = http.createServer(app);

console.log("starting in server for PORT"+port)
server.listen(port);