/*
NN Plots

cvalenzuela
*/

/* todo: add url in about, */

document.addEventListener("deviceready", onDeviceReady, false);

var imageURL;
var ip = 'http://172.16.220.175:8080/'
var upload = ip + "upload";
var id = 1;
var currentImageHolder = null;
var currentImage = null;
var photo = null;

// on device ready
function onDeviceReady() {
  currentImageHolder = document.getElementById('currentImageHolder');
  currentImage = document.getElementById('currentImage');
  $("#currentImageHolder").hide();
  $("#loading").hide();
}

// Use camara
function useCamara() {
  navigator.camera.getPicture(cameraSuccess, cameraError, {
    quality: 20,
    allowEdit: true,
    destinationType: navigator.camera.DestinationType.FILE_URI
  });
};

// Use an existig photo
function getImage() {
  navigator.camera.getPicture(cameraSuccess, cameraError, {
    quality: 20,
    destinationType: navigator.camera.DestinationType.FILE_URI,
    sourceType: navigator.camera.PictureSourceType.PHOTOLIBRARY
  });
}

// Display Image taken/selected
function cameraSuccess(imageData) {
  console.log('Got image')
  imageURL = imageData;
  $("#currentImageHolder").show();
  currentImage.src = imageData;
}

// Upload image to server
function uploadPhoto() {
  // Uncomment this for lstm version
  // lstm();
  $("#loading").show();
  console.log('Upload Image')
  $("#currentImageHolder").hide();
  currentImage.src = '#';
  photo = document.getElementById('photo'+id);
  photo.src = imageURL;
  // Increase the current image/text
  (id < 10) ? id++ : id = 0;

  var options = new FileUploadOptions();
  options.fileKey="file";
  options.fileName=imageURL.substr(imageURL.lastIndexOf('/')+1);
  options.mimeType="image/jpeg";

  var params = new Object();
  params.name = id-1;

  options.params = params;
  options.chunkedMode = true;

  var ft = new FileTransfer();
  ft.upload(imageURL, upload, win, fail, options);
}

// clear all current images
function clearAll(){
  $("#currentImageHolder").hide();
  currentImage.src = '#';

  for (var i = 1; i < 10; i++){
    var img = document.getElementById('photo'+i);
    img.src = 'img/noImage.jpg'
    $("#genPar"+i).text( " " );
  }

  for (var i = 1; i < 10; i++){
    var img = document.getElementById('photo'+i);
    img.src = 'img/noImage.jpg'
  }
  id = 1;
}

// remove the last image
function removePhoto(){
  $("#currentImageHolder").hide();
  currentImage.src = '#';
  if (id > 1){
    id = id - 1
  }
  document.getElementById('photo'+id).src = 'img/noImage.jpg'
}

// Server response after sending image
function win(r) {
  $("#loading").hide();
  var response =  JSON.parse(r.response);
  console.log(r)
  console.log("File Uploaded " + response.status);
  //$("#genTitle").text(response.term);
  Typed.new('#genPar'+(id-1), {
    strings: [response.text],
    typeSpeed: 0,
    showCursor: false,
    contentType: 'text',
  });
}

function fail(error) {
  alert("An error has occurred: Code = " = error.code);
}

function cameraError(){
  alert("Error Classifying Image :(")
}

// this function is just for the lstm server version
function lstm(){
  var base64 = imageURL;
  var cleaned = base64.replace(/data:image\/(png|jpeg|jpg|gif);base64,/, '');
  var data = {
    img: cleaned
  }
  photo.src = "data:image/jpeg;base64," + imageURL;
  //send the data
  $.post(upload, "data", function(response) {
  //  $("#genTitle").text(response.term);
    Typed.new('#genPar', {
      strings: [response.text],
      typeSpeed: 0,
    });
    console.log(response)
  });
}
