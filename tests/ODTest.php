<?php

use PHPUnit\Framework\TestCase;
use Entries\EntriesBuilder;

class ODTest extends TestCase
{
   /**
    *  @dataProvider additionProvider
    */
   public function testOD($expected,$a)
   { 
       $this->assertSame($expected,(new EntriesBuilder($a))->build());
   }

   public function additionProvider()
   { 
       $data = json_decode(file_get_contents('tests/data.json'),true);
       $result = [];

       foreach ($data as $value) {
             $result[] = [$value['result'],$value['data']];
       }  

       return $result;
   }
}
?>