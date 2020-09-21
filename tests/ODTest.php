<?php

require_once realpath('src/autoload.php');
require_once realpath('vendor/autoload.php');

use PHPUnit\Framework\TestCase;
use Entries\EntriesBuilder;

class ODTest extends TestCase
{
   /**
    *  @dataProvider additionProvider
    */
   public function testOD($a,$expected)
   {
       $this->assertSame($expected,(new EntriesBuilder($a))->build());
   }

   public function additionProvider()
   { 
       $data = json_decode(file_get_contents('tests/data.json'),true);
       $headlines = [ "definitions and pronucitions"=>[],"only definitions"=>[],'no results'=>[]];

       foreach (array_slice($headlines,0,2) as $key => $value) {
            $nextItem = $data[next($data)];

            if ($nextItem) {
                array_push($headlines[$key],$nextItem['data'],$nextItem['result']);
            }
       }  

       return $headlines;
   }
}
?>