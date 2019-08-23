// viewer.js for videos 

/////////////  GLOBALS /////////////////////////////
//window.$ = window.jQuery = require('jquery');
var videosDir = '/info/videos/';;

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
function readText(videoDir, meta){
	//console.log ("in readText");
  var resp = $.ajax({
    type: 'GET',
    url: videosDir + videoDir + '/' + meta
  })
  .done(function( data ) {
  	 html = data;
  })
  .fail(function (){
      console.log('readText failed. URL=' + videosDir + videoDir + '/' + meta);
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
