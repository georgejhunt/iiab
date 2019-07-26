// viewer.js for videos 

/////////////  GLOBALS /////////////////////////////
window.$ = window.jQuery = require('jquery');
var metaData = '/library/videos/metadata/';
var videosDir = '/library/videos/content/';;

// initial values for on event variables to get through startup
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}
var path = getUrlParameter('path');
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
   var config = {};
   editor1 = CKEDITOR.appendTo('editor1', config, html);
}


$.when(readText(path)).then(createEditor);
 


