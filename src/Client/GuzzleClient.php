<?php

namespace Main\Client;

abstract class GuzzleClient
{
    protected $client;
    protected const ENDPOINT = 'https://od-api.oxforddictionaries.com:443/api/v2 ';
    protected const API_KEY = '19059878f0026d106c71adddcc19aa7b';
    protected const API_ID = '8722c574';

    public function __construct()
    {
        $this->client = new \GuzzleHttp\Client([
            'base_uri' => self::ENDPOINT,
            'headers' => [
                'Accept' => 'application/json',
                'app_key' => self::API_KEY,
                'app_id' => self::API_ID
            ]
        ]);
    }

    public function get(string $url)
    {
        try {
            return $this->client->get($url)->getBody()->getContents();
        } catch (RequestException $e) {
            throw new ClientException($e->getMessage(), $e->getCode());
        }
    }
}

?>