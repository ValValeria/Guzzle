<?php

require_once realpath('../src/autoload.php');

use PHPUnit\Framework\TestCase;

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
       $data = json_decode(file_get_contents(realpath('data.json')));
       $headlines = [ "defitions and pronuctions"=>[],"only defitions"=>[],'no results'=>[]];

       foreach ($headlines as $key => $value) {
            $nextItem = next($data);
            $headlines[$key]= [$nextItem['data'],$nextItem['result']];
       }

       return $headlines;
   }
}
?>