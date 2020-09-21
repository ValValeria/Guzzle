<?php

function my_autoload ($pClassName) {

     $path = realpath($pClassName . ".php");

     if(strlen($pClassName) && $path){
        include($path);
     }
 }
 
 spl_autoload_register("my_autoload");

?>