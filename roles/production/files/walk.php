<?php
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

$ite=new RecursiveDirectoryIterator("/library/www/html/info/videos");

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
    echo "$fname => $pretty, Duration: $video_time, $modate<br>";
}

$bytestotal=number_format($bytestotal);
echo "Total: $nbfiles files, human_filesize($bytestotal) bytes\n";
?>
