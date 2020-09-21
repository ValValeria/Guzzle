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
            try {
                array_push($entries,$this->buildEntry($item));
            } catch (\InvalidArgumentException $e) {
            }
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
                
                foreach (($item->senses) as $sence) {
                    foreach (($sence->definitions) as $definition) {
                        $entry->addDefinition($definition);
                    }
                }

                foreach (($item->pronunciations) as $pronunciation) {
                    $entry->addPronunciation($pronunciation->audioFile);
                }
            }
        }

        return $entry->toArray();
    }
}

 ?>