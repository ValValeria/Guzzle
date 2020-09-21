<?php

require_once realpath('./autoload.php');
require_once realpath('../vendor/autoload.php');

use Dictionary\Dictionary;

$word = 'how';
$dictionary = new Dictionary();

try {
    $results = $dictionary->entries('en-gb', $word);
    echo $results;
} catch (DictionaryException $e) {
    echo $e->getMessage();
}

?>

