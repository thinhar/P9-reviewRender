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

router.get('/:NAME', (req, res, next) => {
  
  const taskname = req.params.NAME;

  console.log(taskname);
  
    exec('/home/nodejs/analyzer.sh ${taskname}', function(err, stdout, stderr) {
       	if(err) {
            res.status(400).json({
                error: stderr
            });
       	}
        else {
       	    output = stdout;
	    res.status(200).json({
          task: taskname,
	        message: "succesfully analyzed and started task manager",
            });
       	}
   });

});


module.exports = router;