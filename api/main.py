"""Parse data from with https://www.coingecko.com"""

from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel, Field
from requests import request
import json as JSON

app = FastAPI()


class Description(BaseModel):
    en: str


class Coin(BaseModel):
    id: str
    symbol: str
    name: str
    description: Description


@app.get("/")
def read_root():
    return {"Coins": "https://www.coingecko.com"}


"""Coin parse by name. """


@app.get("/coins/{coin_id}/")
def coin(coin_id: str):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    response = request('GET', url).json()
    str_response = JSON.dumps(response)
    parse_response = Coin.parse_raw(str_response)
    data_api = str(dict([data for data in parse_response]))[1:-1]
    return data_api


"""The price of coins. """


@app.get("/coins/price/{id_name}/{cross_rate}")
def coins_price(id_name: str, cross_rate: str):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={id_name.lower()}&vs_currencies={cross_rate.lower()}'
    response = request('GET', url).json()
    return response[f'{id_name}'][f'{cross_rate}']


"""Parse by name or id for all coins. """


@app.get("/coins/list/{id_name}/")
def list_coins_id(id_name: str):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = request('GET', url).json()
    coin_name = [coin.get(id_name) for coin in response]
    return coin_name


"""Parse for all coins in a list."""


@app.get("/coins/all/list/")
def list_coins():
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = request('GET', url).json()
    return response
