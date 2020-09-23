<?php

namespace Main\URLHandler;

use Main\Dictionary\Dictionary;

class URLHandler
{
      public $dictionary;
      public $content;
      
      public function __construct()
      {
        $this->dictionary = new Dictionary();
        $this->content = file_get_contents(realpath('src/Templates/MainPage.blade.php'));
      }

      public function getMainPage()
      {
        $results = [];  
        return eval( '?> '.$this->content.' <?php ' );
      }

      public function findWord($word,$error=false)
      {
        try {
            if(!$error){
              $results = $this->dictionary->entries('en-gb', $word);
            }
        } catch (\Throwable $e) {
            $error = true;
        }
        
        return eval( '?> '.$this->content.' <?php ' );
      }

}

?>