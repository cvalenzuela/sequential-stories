/*
NN Plots

cvalenzuela
*/

/* todo: add url in about, */

document.addEventListener("deviceready", onDeviceReady, false);

var imageURL;
var ip = '0'
var upload = ip + "upload";
var id = 1;
var currentImageHolder = null;
var currentImage = null;
var photo = null;
var readyToUpload = false;

// getIp
$("#menu").click(function() {
  $("#getIp").show();
});

$("#submitIp").click(function() {
  ip = 'http://' +  $('#ip').val() + ':8080/';
  upload = ip + "upload";
  $("#getIp").hide();
  console.log('submit to ip: ' + ip)
  $.ajax({
    type: "GET",
    url: ip,
    success: function(msg){
      $("#status").css("background-color", "#2dc377");
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      $("#status").css("background-color", "#c32d2d");
    }
  });
});

// on device ready
function onDeviceReady() {
  currentImageHolder = document.getElementById('currentImageHolder');
  currentImage = document.getElementById('currentImage');
  $("#currentImageHolder").hide();
  $("#loading").hide();
  $("#getIp").hide();
  for (var i = 7; i < 10; i++){
    $("#element"+i).css("display", "none");
  }
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
  $("#usePhoto").css("background", "#4ac78e");
  readyToUpload = true;
}

// Upload image to server
function uploadPhoto() {
  // Uncomment this for lstm version
  // lstm();
  if(readyToUpload){
    readyToUpload = false;
    $("#loading").show();
    $("#usePhoto").css("background", "rgba(0, 0, 0, 0.31)");
    console.log('Upload Image')
    $("#currentImageHolder").hide();
    currentImage.src = '#';
    photo = document.getElementById('photo'+id);
    photo.src = imageURL;
    $("#element"+id).css("display", "inline-block");

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
  else{
    navigator.notification.alert("Please Select an Image to Upload", function(){
      $("#loading").hide();
    }, "No Image", "Got it!")
  }
}

// clear all current images
function clearAll(){
  $("#currentImageHolder").hide();
  currentImage.src = '#';
  $("#loading").hide();

  for (var i = 1; i < 10; i++){
    var img = document.getElementById('photo'+i);
    img.src = '#'
    $("#genPar"+i).text( " " );
  }
  $("#genTitle").text( " " );

  for (var i = 7; i < 10; i++){
    $("#element"+i).css("display", "none");
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
  if(id-1 == 1){
    $("#genTitle").text(response.title);
  }

  Typed.new('#genPar'+(id-1), {
    strings: [response.text],
    typeSpeed: 0,
    showCursor: false,
    contentType: 'text',
  });
}

function fail(error) {
  navigator.notification.alert("Please add a valid IP address", function(){
    $("#loading").hide();
  }, "An Error has Occurred", "Got it!")
  //alert("An error has occurred: Code = " + error.code);
}

function cameraError(){
  // navigator.notification.alert("Couldn't classify this image", function(){
  //   $("#loading").hide();
  // }, "An Error has Occurred", "Got it!")
  //alert("Error Classifying Image :(")
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
  $.post(upload, data, function(response) {
  //  $("#genTitle").text(response.term);
    Typed.new('#genPar', {
      strings: [response.text],
      typeSpeed: 0,
    });
    console.log(response)
  });
}
