<?php
   $video_base = '/library/www/html/info/videos';
   $video_url = '/info/videos';

function human_filesize($bytes, $decimals = 1) {
    $size = array('B','kB','MB','GB','TB','PB','EB','ZB','YB');
    $factor = floor((strlen($bytes) - 1) / 3);
    return sprintf("%.{$decimals}f", $bytes / pow(1024, $factor)) . @$size[$factor];
}

function getDuration($file){
   include_once("/usr/share/php/getid3/getid3.php");
   $getID3 = new getID3;
   $file = $getID3->analyze($file);
   return $file['playtime_string'];
}
function getOneLine($file){
  $lines = file($file);
  if ($lines !== FALSE) return $lines[0]; else return '';
}
  
function getLines($file){
  $lines = file($file);
  if ($lines !== FALSE) return $lines; else return [];
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
    <link rel="stylesheet" href="./viewer.css" type="text/css">
    <script src="/common/js/jquery.min.js">
      window.$ = jQuery;
    </script>
    <script src="./video.js"></script>
  </head>

  <body>
      <div class = "h1" id="headerDesktop" style="align: center;">Internet in a Box -- HowTo Videos</div> 
    <!--<div id="content" class="flex-col"> -->
    <!--<div class="content-item"> -->
<?php
$iter=new RecursiveDirectoryIterator($video_base);

$bytestotal=0;
$nbfiles=0;
$menuhtml =  '<div class="content-item" >';
foreach (new RecursiveIteratorIterator($iter) as $filename=>$cur) {
  if (is_dir($cur) && substr($cur,-1,1) != '.'){
    $heading = basename($cur);
    $menuhtml .= "<h1>$heading</h1>";
    continue;
  }
    $regex = "@/([A-Za-z0-9-_.]+/)([A-Za-z0-9-_.]+/)([A-Za-z0-9-_.]+)(\.mp4|m4v|mov)$@";
    preg_match($regex,$cur,$matches);
    if ( ! $matches ) continue;
    //die(print_r($matches));
    $fname = $matches[2] . $matches[3] . $matches[4];
    $after_video = $fname;
    if ($matches[1] !== 'videos') $after_video = "$matches[1]/$fname";
    $href = $video_url . "/viewer.php?name=" . $after_video;
    $category_dir = $matches[1]; 
    if ($category_dir == 'videos/')  $category_dir = '';
    $path = $video_base . "$category_dir/$matches[3]";
    $title = getOneLine("$path/title");
    if ($title === '') $title = $fname;
    $video_link = "<a href=$href >$title</a>";
    $oneliner = getOneLine("$path/oneliner");
    $filesize=$cur->getSize();
    $bytestotal+=$filesize;
    $nbfiles++;
    $pretty = human_filesize($filesize);
    $video_time = getDuration($filename);
    $modate = date ("F d Y", filemtime($filename));
    $menuhtml .= "<br>$video_link -- $oneliner <br>   $pretty, Duration: $video_time h:m:s, $modate<br>";
}
$bytestotal=human_filesize($bytestotal);
$menuhtml .= "<br>Total: $nbfiles files,  $bytestotal . bytes\n";
$menuhtml .= "</div>";
echo $menuhtml;
?>
<!--   </div>  End content-->
<!--   </div> flex-col -->
</body>
</html>
