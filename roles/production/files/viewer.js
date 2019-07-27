// viewer.js for videos 

/////////////  GLOBALS /////////////////////////////
//window.$ = window.jQuery = require('jquery');
var metaData = '/library/videos/metadata/';
var videosDir = '/library/www/html/local_content/';;

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
var path = getUrlParameter('name');
if ( path == '') {
   alert('Please specify "name=" in URL');
   exit();
}

var html, editor1 = '';
function readText(path){
	//console.log ("in readText");
  var resp = $.ajax({
    type: 'GET',
    url: metaData + path,
    dataType: 'text/html'
  })
  .done(function( data ) {
  	 html = data;
  })
  .fail(function (){
      consoleLog('readText failed');
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
   html = "Path is " + path;
   editor1 = CKEDITOR.appendTo('editor1', config, html);
}


$.when(readText(path)).then(createEditor);
 
createEditor();

$( #save ).on('click',function(){
    if ( ! path ){
      alert("please specify a filename to save");
      return;
    }
    var data = CKEDITOR.instances.editor1.getData();
   $.ajax({
     type: "POST",
     url: './videos/writer',
     data: data,
     fail: function(data){
      alert('Failed to write ' + path)
     },
     dataType: 'html'
   }); 
})
