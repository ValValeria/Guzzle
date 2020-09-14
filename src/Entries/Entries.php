<?php

namespace Entries;

class Entries 
{
    private $definitions = [];

    private $pronunciations = [];
    
    /**
     * @return array
     */
    public function getDefinitions(): array
    {
        return $this->definitions;
    }

    /**
     * @return array
     */
    public function getPronunciations(): array
    {
        return $this->pronunciations;
    }


      /**
     * @param $definition
     *
     * @return $this
     */
    public function addDefinition($definition)
    {
        if (!in_array($definition, $this->definitions)) {
            $this->definitions[] = $definition;
        }

        return $this;
    }

    /**
     * @param $link
     *
     * @return $this
     */
    public function addPronunciation($link)
    {
        if (!in_array($link, $this->pronunciations)) {
            $this->pronunciations[] = $link;
        }

        return $this;
    }


    public function toArray()
    {
        return [
            'definitions' => $this->definitions,
            'pronunciations' => $this->pronunciations,
        ];
    }
}


?>


