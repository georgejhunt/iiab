<?php
   $video_base = '/info/videos';
   if ( ! isset($_REQUEST['name'])){
      echo('Please enter the video name as a "name=blah" parameter');
      exit(1);
   } else {
      if ( isset($_REQUEST['suffix']))
         $suffix = $_REQUEST['suffix'];else $suffix = 'mp4';
      if (substr($suffix,0,1) == '.') $suffix = substr($suffix,1);
      //name may include a category in path preceeding video directory specifier
      $video_name = $_REQUEST['name'];
      $video_basename = basename($video_name);
      $video_dirname = dirname($video_name);
      if ($video_dirname != '.') $video_dirname = $video_dirname . '/';else $video_dirname = "";
      $video_stem = pathinfo($video_name, PATHINFO_FILENAME);
      $video_full_path = "$video_base/$video_dirname$video_stem/$video_basename.$suffix";
   }
?>
<!DOCTYPE html>
<html>
  <head>

    <title>Internet in a Box - Videos</title>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="/common/css/fa.all.min.css"/>
    <link rel="stylesheet" href="/common/css/font-faces.css"/>
    <link rel="stylesheet" href="./viewer.css" type="text/css">
    <script src="/common/js/jquery.min.js"></script>
    <script src="/ckeditor/ckeditor.js" type="text/javascript"></script>
  </head>

  <body>
    <div class="wrapper">
      <div id="mainOverlay" class="overlay"></div>
      <div class="flex-col">
      <div class = "h1" id="headerDesktop" style="align: center;">Internet in a Box</div> 
        <div id="content" class="flex-col">
            <div id="video_div" class="row">
               <video width="854" height="480" align="center" controls>
                 <source src="
                  <?php echo($video_full_path);?>
                  " type="video/mp4">
                 Your browser does not support the video tag.
               </video>
            </div>
            <span>
            Filename:
            <input id="filename" name="filename" type="text">
            <button id="New File" value="save">New File</button>
            <button id="Overwrite" value="save">Overwrite</button>
            <button id="save" value="save">Save</button>
            </span>
            <div id="editor1" class="row">
            </div> <!-- End editor1 -->
            <div id="description">
            </div>
            <h3>Spoken Text</h3>
            <div id="lang_buttons"> </div>
            <div id="closed_captions"></div>
        </div> <!-- End content container -->
      </div> <!-- Flex -->
    </div> <!-- Wrapper -->
  <script src="./static/viewer.js" type="text/javascript"></script>
  </body>
</html>
