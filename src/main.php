<?php

require_once '../vendor/autoload.php';

use Main\URLHandler\URLHandler;

$handler = new URLHandler();
$method = $_SERVER['REQUEST_METHOD'];

if($method == "GET"){

   echo $handler->getMainPage();

} else if ($method == "POST") {

      $isError = false;

      if (strlen($_POST['word'])>=3 && strlen($_POST['word'])<=20) {
          $isError = true;
      }

      echo $handler->findWord($_POST['word'],$isError);
} else {
   http_response_code(404);
}


?>

