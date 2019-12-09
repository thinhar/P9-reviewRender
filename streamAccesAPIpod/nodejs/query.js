const express = require('express');
const router = express.Router();

var exec = require('child_process').exec,child;

//router.get('/:URL/:UA/:DELETECOOKIES', (req, res, next) => {
//exec(`./P7-DimensionalShopping/Backend/callQueryWithUser.sh ${curURL} ${curUA} ${curDELETECOOKIES}`, function(err, stdout, stderr) {

router.get('/pig', (req, res, next) => {
    exec(`/home/nodejs/dummyScript.sh pig`, function(err, stdout, stderr) {
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


router.get('/stream/:STREAMNAME', (req, res, next) => {

  const streamName = req.params.STREAMNAME;

  console.log(streamName);
  htmlReturnText= '<html> <head> <meta name="viewport" content="width=device-width"> </head><body><video controls name="media"><source src="/home/shared/'+streamName+'/output.webm" type="video/webm">Your browser doesnt support HTML5 video tag.</video></body></html>';


  res.status(200).send(htmlReturnText);

});
router.get('/stream/:STREAMNAME/data', (req, res, next) => {

  const streamName = req.params.STREAMNAME;

  res.setHeader("content-type", "some/type");
  fs.createReadStream("/home/shared/"+streamName+"output.webm").pipe(res);

});



module.exports = router;