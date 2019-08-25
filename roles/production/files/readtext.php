<?php
   $video_base = '/library/www/html/info/videos';
   $video_url = '/info/videos';
   if ( ! isset($_REQUEST['name'])){
      echo('Please enter the video name as a "name=blah" parameter');
      exit(1);
   } 

   //name may include a category in path preceeding video directory specifier
   $file_name = $_REQUEST['name'];
   $file_path = "$video_base/$file_name";

   $file = fopen($file_path, "r");

   //Output lines until EOF is reached
   while(! feof($file)) {
     $line = fgets($file);
     echo $line. "<br>";
   }

   fclose($file);
?>
