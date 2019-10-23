const express = require('express');
// Web framework for nodejs, a layer that we use for HTTP requests 
const app = express();
const morgan = require('morgan');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload');
// HTTP request logging for nodejs, useful for debugging 

const queryRoutes = require('./query');
app.use(morgan('dev')); 
// Log information dev style

// enable files upload
app.use(fileUpload({
    createParentPath: true
}));

app.use(BodyParser.json);


app.use('/query', queryRoutes);
// All requests by name /query should be handled by queryRoutes

app.use((req, res, next) => {
	const error = new Error('not found');
	error.status = 404;
	next(error);
})
// Send error if we cant find the correct endpoint

app.use((error, req, res, next) => {
	res.status(error.status || 500);
	res.json({
		error: {
			message: error.message
		}
	});
});
// "catch" errors and display the error message
// Error code 500 if it doesnt have a error code defined prior

module.exports = app;