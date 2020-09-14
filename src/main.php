<?php

require_once realpath('vendor/autoload.php');
require_once realpath('src/autoload.php');

use \Dictionary\Dictionary;

$word = 'how';
$dictionary = new Dictionary();

try {
    $results = $dictionary->entries('en-gb', $word);
} catch (DictionaryException $e) {
    echo $e->getMessage();
}

?>