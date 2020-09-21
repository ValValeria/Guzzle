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
                "/api/v2/entries/$lang/$word?strictMatch=false",
            ));

        } catch (ClientException $e) {
            switch ($e->getCode()) {
                case 404:
                    $data = null;
                    return;
                default:
                    throw new DictionaryException('Something went wrong');
            }
        } finally {
            $results = $data->results ?? [];
        }

       return json_encode((new EntriesBuilder($results))->build(),JSON_UNESCAPED_UNICODE);
    }
}


?>