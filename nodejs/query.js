const express = require('express');
const router = express.Router();
const uuidv4 = require("uuid/v4")
var fs = require('fs');

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

//exec("/usr/bin/amqp-declare-queue --url=$BROKER_URL -q "+sampleFile.name+" && /usr/bin/amqp-publish --url=$BROKER_URL -r "+sampleFile.name+" -p -b \""+sampleFile.name +" -f 1\"  && /usr/bin/amqp-publish --url=$BROKER_URL -r $QUEUE -p -b "+sampleFile.name, function(err, stdout, stderr) {
 

router.post('/upload/:REQUESTEDFRAMERATE', function(req, res, next) {
  //console.log(req.files);
  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No file was uploaded.');
  }

  let analyzerService_ip = process.env.ANALYZER_SERVICE_SERVICE_HOST;
  
  const requestedframerate = req.params.REQUESTEDFRAMERATE;
  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
  let sampleFile = req.files.theFile;
  taskname=uuidv4();
  console.log(analyzerService_ip+" "+sampleFile.name+" "+ taskname);

  sampleFile.mv('/home/shared/'+taskname+'.blend', function(err, stdout, stderr) {
    if(err) {
        res.status(400).json({
            error: stderr
        });
    }
    else {

      exec("mkdir -p /home/shared/"+taskname+" && date --utc +%FT%T.%3NZ > /home/shared/"+taskname+"/timestamps && curl --request GET "+analyzerService_ip+":80/query/"+requestedframerate+"/"+ taskname+ ".blend ", function(err2, stdout2, stderr2) {
        if (err2){
          return res.status(500).json({
            error : stderr2});
        }else { 
          res.status(200).json({
              name: sampleFile.name,
              mimetype: sampleFile.mimetype,
              size: sampleFile.size,
			  taskName: taskname,
              message: "uploaded"
          });
        }
      });
    }
  });

  // Use the mv() method to place the file somewhere on your server
  
  //console.log(req.files.foo.name); // the uploaded file object
});
router.get('/stream/:STREAMNAME/currentdata', (req, res, next) => {
    const streamName = req.params.STREAMNAME;

      exec("cat /home/shared/"+streamName+"/currentFinalfile", function(err, stdout, stderr) {
        if (err) {
            res.status(400).json({
                error: stderr
            });
        }
        else {
            outputfilename=stdout;
            res.setHeader("content-type", "video/webm");
            fs.createReadStream("/home/shared/"+streamName+"/"+outputfilename+"").pipe(res);
        }
      });




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