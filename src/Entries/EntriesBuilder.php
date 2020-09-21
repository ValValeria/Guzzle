<?php

namespace Entries;

use Entries\Entries as Entry;

class EntriesBuilder
{
    private $data;

    public function __construct($data)
    {
        $this->data = $data;
    }

    /**
     * @return Entry[]
     */
    public function build() : array
    {
        $entries = [];

        foreach ($this->data as $item) {
            array_push($entries,$this->buildEntry($item));
        }

        return $entries;
    }

    /**
     * @param $response
     *
     * @return Entry
     */
    private function buildEntry($response)
    {
        $entry = new Entry();
            
        foreach ($response->lexicalEntries as $lexicalEntry) {
            foreach ($lexicalEntry->entries as $item) {
                
                if (property_exists($item,'senses')){
                    foreach (($item->senses) as $sence) {
                        foreach (($sence->definitions) as $definition) {
                            $entry->addDefinition($definition);
                        }
                    }
                }

                if (property_exists($item,'pronunciations')) {
                    foreach (($item->pronunciations) as $pronunciation) {
                        $entry->addPronunciation($pronunciation->audioFile);
                    }
                } 
            }
        }

        return $entry->toArray();
    }
}

 ?>