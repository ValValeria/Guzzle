<?php

namespace Dictionary;

use Client\GuzzleClient as Client;
use Entries\EntriesBuilder;
use Dictionary\DictionaryException;

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
        try {
            
            $data = json_decode($this->get(
                "/api/v2/entries/$lang/$word?fields=definitions%2Cpronunciations&strictMatch=false",
            ),true);

        } catch (ClientException $e) {
            if($e->getCode()>299){
                throw new DictionaryException('Something went wrong');
            }
        } finally {
            $results = is_array($data['results'])?$data['results'] : [];
        }

        return json_encode((new EntriesBuilder($results))->build(),JSON_UNESCAPED_UNICODE);
    }
}


?>