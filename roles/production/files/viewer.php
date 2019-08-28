<?php
   $video_base = '/library/www/html/info/videos';
   $video_url = '/info/videos';
   if ( ! isset($_REQUEST['name'])){
      echo('Please enter the video name as a "name=blah" parameter');
      exit(1);
   } else {
      $suffix = '.mp4';

      //name may include a category in path preceeding video directory specifier
      $video_name = $_REQUEST['name'];
      $video_basename = basename($video_name);

      // look for video extension
      $index = strpos($video_basename,'.');
      if ( $index ) {
         $suffix = substr($video_basename,$index);      
         $video_basename = substr($video_basename,0,$index);
      }

      // look for a category (folder name) preceeding actual filename
      $video_dirname = dirname($video_basename);
      if ($video_dirname != '.') $video_dirname = $video_dirname . '/';else $video_dirname = "";
      $video_stem = pathinfo($video_name, PATHINFO_FILENAME);
      $url_full_path = "./$video_dirname$video_stem/$video_basename$suffix";
      $full_path = "$$video_base/$video_dirname$video_stem";

   }
   chdir("$video_base/$video_dirname$video_basename");
   $vtt_files = glob("*.vtt");
   $langs = array();
   foreach ($vtt_files as $f){
      $langs[] = substr($f,-6,2);
   }
   $langs_count = count($langs);
   // find any images to use as poster
   $cwd = getcwd();
   chdir("$video_base/$video_dirname$video_basename");
   $poster = glob("*.{jpg,jpeg,png}",GLOB_BRACE);
   if ( count($poster) > 0 ) $poster = $poster[0]; else $poster = '';
   chdir($cwd);
   //die(print_r($langs));
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
    <link href="./video-js.css" rel="stylesheet">
    <link rel="stylesheet" href="/js-menu/menu-files/css/js-menu-item.css" type="text/css">
    <script src="/common/js/jquery.min.js">
      window.$ = jQuery;
    </script>
    <script src="./video.js"></script>
  </head>

  <body>
    <div class="wrapper">
      <div id="mainOverlay" class="overlay"></div>
      <div class="flex-col">
      <div class = "h1" id="headerDesktop" style="align: center;">Internet in a Box</div> 
        <div id="content" class="flex-col">
           <div id="video_div">
              <video id="example_video_1" class="video-js" controls preload="none" :
               width="720" height="540" poster='<?php echo("./$video_dirname$video_stem/$poster");?>' data-setup="{}">
               <source src="<?php echo($url_full_path);?>" type="video/mp4">
               <?php
                  for ( $i=0; $i<$langs_count; $i++){ 
                     $src = "./$video_dirname$video_stem/$vtt_files[$i]"; 
               ?>
               <track kind="captions" src="<?=$src?>" srclang="en" label="<?=$langs[$i]?>">
               <?php } ?>
               <p class="vjs-no-js">To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="https://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a></p>
              </video>


            </div> <!-- video-div -->
            <fieldset>
              <legend>MetaData</legend>
            <table style="text-align: left"><tr><td>
            Title:</td><td>
            <input id="title" size="64" name="title" type="text"></td></tr><tr><td>
            One line description:</td><td>
            <input id="oneliner" name="oneliner" type="text" size="80"></td></tr>
            <tr><td>Details:</td><td>
               <textarea id="Detail" cols="80" rows="10">
               </textarea></td></tr>
            </table>
            </fieldset>
            <h3>Spoken Text:</h3>

            <div id="details">
               <textarea id="translation" cols="120" rows='15'>
               </textarea>
            </div>
            <div id="editor1" class="row">
            </div> <!-- End editor1 -->
               <?php
                  for ( $i=0; $i<$langs_count; $i++){ 
                     $src = "./$video_dirname$video_stem/$vtt_files[$i]"; 
                     $lang = $langs[$i];
               ?>
            <?php } ?>
            <button id="save" value="save">Save</button>
            <script>
               window.details = <?php echo "$video_dirname$video_stem/details";?>;
               window.langs = <?php json_encode($langs); ?>;
               window.vtt_files = <?php echo $vtt_files; ?>;
               window.full_path = <?=$full_path?>;
            </script>
            <div id="lang_buttons"> </div>
            <div id="closed_captions"></div>
        </div> <!-- End content container -->
      </div> <!-- Flex -->
    </div> <!-- Wrapper -->
  <script src="./viewer.js" type="text/javascript"></script>
  </body>
</html>
