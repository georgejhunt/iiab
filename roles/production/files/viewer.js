// viewer.js for videos 

/////////////  GLOBALS /////////////////////////////
//window.$ = window.jQuery = require('jquery');
var videosDir = '/info/videos/';;

/////////////  FUNCTIONS  /////////////////////////////
function UrlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status!=404;
}

function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

var videoDir = getUrlParameter('name');
if ( videoDir == '') {
   alert('Please specify "name=" in URL');
   exit();
}

var html, editor1 = '';
function readText(videoDir, fname){
	//console.log ("in readText");
  var resp = $.ajax({
    type: 'GET',
    url: videosDir + 'readtext.php?name=' + fname
  })
  .done(function( data ) {
  	 html = data;
  })
  .fail(function (){
      console.log('readText failed. URL=' + videosDir + 'readtext.php?name=' + fname);
      html = '';
  })
  return resp;
}

function createEditor(html) {
   if (editor1)
     return;

   // Create a new editor instance inside the <div id="editor"> element,
   // setting its value to html.
   var config = {"rows":"10","cols":"80"};
   //html = "Path is " + videoDir;
   editor1 = CKEDITOR.appendTo('editor1', config, html);
}

var meta = "details";
$.when(readText(videoDir,meta)).then(function(data,textStatus,jqXHR){
     createEditor(data);
});
 
//createEditor();

$( "#save" ).click(function(){
    if ( ! videoDir ){
      alert("please specify a filename to save");
      return;
    }
    var data = CKEDITOR.instances.editor1.getData();
   $.ajax({
     type: "POST",
     url: './videos/writer',
     data: data,
     fail: function(data){
      alert('Failed to write ' + videoDir)
     },
     dataType: 'html'
   }); 
})


function get_translations(video_path,lang=''){
  var resp = $.ajax({
    type: 'GET',
    dataType: 'json',
    url: videosDir + 'readtext.php?name=' + fname + lang
  })
  .done(function( data ) {
  	 html = data;
  })
  .fail(function (){
      console.log('get_translations failed. URL=' + videosDir + 'readtext.php?name=' + fname);
      html = '';
  })
  return resp;
}
//$.when(get_translations(videoDir,meta)).then(function(data,textStatus,jqXHR){
//     createEditor(data);
//});

$.when(readText(videoDir, window.details)).then(function(data,textStatus,jqXHR){
   $( "#details" ).html = data;
})

// Fill in the blanks
console.log("title:" + window.full_path);