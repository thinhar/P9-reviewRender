const express = require('express');
const router = express.Router();

var exec = require('child_process').exec,child;

router.post('/uploadasync', async (req, res, next) => {
  
  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
  let sampleFile = req.files.theFile;

  // Use the mv() method to place the file somewhere on your server
  sampleFile.mv('/home/shared/'+sampleFile.name, function(err) {
    if (err){
      return res.status(500).json({
        error : err});
    }else {
            res.status(200).json({
                name: sampleFile.name,
                mimetype: sampleFile.mimetype,
                size: sampleFile.size,
                message: "uploaded"
            });
        }
  });

});

router.post('/upload', function(req, res, next) {


  //console.log(req.files);
  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }



  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
  let sampleFile = req.files.theFile;
  exec("/usr/bin/amqp-publish --url=$BROKER_URL -r $QUEUE -p -b "+sampleFile.name, function(err, stdout, stderr) {
    if(err) {
        res.status(400).json({
            error: stderr
        });
    }
    else {
      sampleFile.mv('/home/shared/'+sampleFile.name, function(err2) {
        if (err2){
          return res.status(500).json({
            error : err2});
        }else {
          res.status(200).json({
              name: sampleFile.name,
              mimetype: sampleFile.mimetype,
              size: sampleFile.size,
              message: "uploaded"
          });
        }
      });
    }
  });

  // Use the mv() method to place the file somewhere on your server
  
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