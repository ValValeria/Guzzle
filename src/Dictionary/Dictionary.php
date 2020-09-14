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
    public function entries(string $lang, string $word) : array
    {
        try {
            $data = $this->client->get(
                "/api/v2/entries/$lang/$word?fields=pronunciations&strictMatch=false",
            );
        } catch (ClientException $e) {
            switch ($e->getCode()) {
                case 404:
                    $data = null;
                    break;
                default:
                    throw new DictionaryException('Something went wrong');
            }

        }

       return (new EntriesBuilder($data))->build();
    }
}


?>