<?php

require_once realpath('vendor/autoload.php');

use Main\URLHandler\URLHandler;

$handler = new URLHandler();
$method = $_SERVER['REQUEST_METHOD'];

if($method == "GET"){

   echo $handler->getMainPage();

} else if ($method == "POST") {

      $isError = false;

      $isValidWord = filter_var($_POST['word'], FILTER_SANITIZE_STRING,['options' => array(
         'min_range' => 3,
         'max_range' => 20
      )]);

      if (!$isValidWord) {
          $isError = true;
      }

      echo $handler->findWord($_POST['word'],$isError);
} else {
   http_response_code(404);
}


?>

