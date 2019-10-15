const express = require('express');
const router = express.Router();

var exec = require('child_process').exec,child;

router.post('/upload', function(req, res, next) {

        if (err) {
            res.status(400).json({
                error: stderr
            });
        }
        else {
          output = console.log(req.files.foo.name); 
            res.status(200).json({
                message:        "Result from backend",
                output:         output
            });
        }
  //console.log(req.files.foo.name); // the uploaded file object
});

router.get('/', (req, res, next) => {
    exec('date', function(err, stdout, stderr) {
       	if(err) {
            res.status(400).json({
                error: stderr
            });
       	}
        else {
       	    output = stdout;
	    res.status(200).json({
	        message: "Hello",
       	        date: output
            });
       	}
   });
});

router.get('/pig', (req, res, next) => {
    exec(`./dummyScript.sh pig`, function(err, stdout, stderr) {
        if (err) {
            res.status(400).json({
                error: stderr
            });
        }
        else {
            res.status(200).json({
                message:        "Result from backend",
                output:         stdout
            });
        }
    });
});

module.exports = router;