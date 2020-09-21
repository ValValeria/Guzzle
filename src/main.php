<?php

require_once '../vendor/autoload.php';

use Dictionary\Dictionary;


$word = 'how';

$dictionary = new Dictionary();

try {
    $results = $dictionary->entries('en-gb', $word);
    echo $results;
} catch (Throwable $e) {
    echo "Line: ".$e->getLine()."<br/>";
    echo "Filename: ".$e->getFile()."<br/>";
    echo $e->getMessage();
}

?>

