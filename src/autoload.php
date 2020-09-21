<?php

function my_autoload ($pClassName) {
     include(realpath($pClassName . ".php"));
 }
 
 spl_autoload_register("my_autoload");

?>