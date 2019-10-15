const express = require('express');
const router = express.Router();

const fileUpload = require('express-fileupload');
const app = express();
app.use(fileUpload());

var exec = require('child_process').exec,child;

router.post('/upload', function(req, res, next) {
  console.log(!req.formdata);
  if (!req.formdata || Object.keys(req.formdata).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
  let sampleFile = req.formdata.justStuff;

  // Use the mv() method to place the file somewhere on your server
  sampleFile.mv('/home/filename.jpg', function(err) {
    if (err){
      return res.status(500).send(err);
    }else {
            res.status(200).json({
                message: "uploaded"
            });
        }
  });
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