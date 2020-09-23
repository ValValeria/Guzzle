<?php

namespace Main\Dictionary;

use Main\Client\GuzzleClient as Client;
use Main\Entries\EntriesBuilder;
use Main\Dictionary\DictionaryException;

class Dictionary extends Client
{
    
    /**
     * @param  string  $lang
     * @param  string  $word
     *
     * @return Entry[]
     * @throws DictionaryException
     */
    public function entries(string $lang, string $word)
    {
        $data = [];
        try {
            
            $data = json_decode($this->get(
                "/api/v2/entries/$lang/$word?fields=definitions%2Cpronunciations&strictMatch=false",
            ),true);

            $results = $data['results'] ?? [];

        } catch (\Throwable $e) {
            if($e->getCode()>299){
                throw new DictionaryException('Something went wrong');
            }
        } 
        return (new EntriesBuilder($results))->build();
    }
}


?>