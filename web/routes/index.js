var express = require('express');
var router = express.Router();
var util = require("util");
var fs = require("fs"); 
var multer = require('multer');

var upload       = multer();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Facial Expression Recognition', result: 'Smile' });
});

router.post('/', upload.single('photo'), function (req, res, next) {
  if (req.file) {
    console.log(util.inspect(req.file));
    res.render('index', {photo: req.file.buffer.toString('base64')});
	} else {
    return next(new Error("Hey, first would you select a file?"));
  }
//   var image = './public/images/' + req.files.person.image.name

//   var tmp_path = req.files.person.image.path;
//   var target_path = './public/images/' + req.files.person.image.name;

//   fs.rename(tmp_path, target_path, function (err) {
//    if (err) {
//      return next(new Error(err));
//    }

//    fs.unlink(tmp_path, function (err) {
//      if (err) {
//        console.log(err);
//      }

//      person.save(function (err) {
//        if (err) {
//          return next(new Error(err.message));
//        }

//        res.redirect('/');
//      });
//    });
//  });
});

module.exports = router;
