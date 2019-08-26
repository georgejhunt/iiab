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
    <div id="content" class="flex-col">
    <div class="content-item">
<?php
$ite=new RecursiveDirectoryIterator($video_base);

$bytestotal=0;
$nbfiles=0;
foreach (new RecursiveIteratorIterator($ite) as $filename=>$cur) {
    $regex = "@/([A-Za-z0-9-_.])+\.(mp4|m4v|mov)$@";
    preg_match($regex,$cur,$matches);
    if ( ! $matches ) continue;
    $fname = $matches[0];
    $filesize=$cur->getSize();
    $bytestotal+=$filesize;
    $nbfiles++;
    $pretty = human_filesize($filesize);
    $video_time = getDuration($filename);
    $modate = date ("F d Y", filemtime($filename));
    echo "$fname => $pretty, Duration: $video_time h:m:s, $modate<br>";
}

$bytestotal=number_format($bytestotal);
echo "Total: $nbfiles files, human_filesize($bytestotal) bytes\n";
?>
   </div> <!-- End content-->
   <div class="content-item">
   Hi George
   </div> <!-- End content-->

   </div> <!-- flex-col -->
</body>
</html>
