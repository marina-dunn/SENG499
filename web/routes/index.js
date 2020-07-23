var express = require('express');
var router = express.Router();
var util = require("util");
var fs = require("fs"); 
var multer = require('multer');
const path = require("path")
const http = require("http")
// const nj = require('numjs');
const FormData = require('form-data');
const fetch = require('node-fetch');
const https = require('https');
 
async function run(inputPhoto, res) {
  const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
  });
  const form = new FormData();
  form.append('photo', inputPhoto, {
    contentType: 'image/jpeg',
    filename: 'inputPhoto.jpg',
  });
  console.log('Fetching from middle man')
  const response = await fetch(`https://127.0.0.1:4000`, { method: 'POST', body: form, agent: httpsAgent })
  const data = await response.text();
  console.log(data)
  if (data.startsWith('Error')) {
    res.render('index', {photo: inputPhoto.toString('base64'), error: data});
  } else {
    res.render('index', {photo: inputPhoto.toString('base64'), result: data});
  }
}

var upload       = multer();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Facial Expression Recognition' });
});

router.post('/', upload.single('photo'), async function (req, res, next) {
  if (req.file) {
    console.log(util.inspect(req.file));
    const val = await run(req.file.buffer, res)
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
