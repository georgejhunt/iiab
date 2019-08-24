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

var meta = "description";
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

function video_div(src, poster, langs, transcripts){
   var video_div = '<video id="example_video_1" class="video-js" controls ' +
               'preload="none" width="720" height=540" poster="' + poster +
               '" data-setup="{}"> <source src="' + src + '" type="video/mp4">';
   for (var i=0; i++; i<langs.length){
               video_div += '<track kind="captions" src="' + transcripts[i] +
               '" srclang="en" + ' label=" + langs[i] + ">';
   }
   video_div += '<p class="vjs-no-js">To view this video please enable JavaScript, ' +
                'and consider upgrading to a web browser that ' +
                '<a href="https://videojs.com/html5-video-support/" target="_blank">' +
                'supports HTML5 video</a></p></video>';
   return video_div;
} 

function get_translations(video_path,lang=''){
  var resp = $.ajax({
    type: 'GET',
    dataType: 'json',
    url: videosDir + 'readtext.php?name=' + fname + lang;
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
$.when(get_translations(videoDir,meta)).then(function(data,textStatus,jqXHR){
     createEditor(data);
});

// load the video div -- what are the particulars for this video?
$( "#video_div" ).html = video_div(videosDir + '/' +videoDir,
