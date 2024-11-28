# -*- coding: utf-8 -*-
# @Author  : kelvin.chiu021@gmail.com
# @Time    : 2024/11/28 13:50
# @Desc    : Cryptocurrency data model and request params and headers factory for Yahoo Finance API

import os
from typing import List

import dotenv


dotenv.load_dotenv(dotenv_path='./.env')


class SymbolContent:
    """
    Basic symbol content container
    """
    symbol: str = ""  # symbol
    name: str = ""  # name
    price: str = ""  # price
    change_price: str = ""  # change price
    change_percent: str = ""  # change percent
    market_price: str = ""  # market price

    def __str__(self):
        return f"""
            Symbol: {self.symbol}
            Name: {self.name}
            Price: {self.price}
            Change Price: {self.change_price}
            Change Percent: {self.change_percent}
            Market Price: {self.market_price}
        """

    @classmethod
    def get_fields(cls) -> List[str]:
        return [
            field for field in cls.__dict__.keys() if not field.startswith("__")
        ]


def request_params_and_headers_factory():
    """
    Request params and headers factory for Yahoo Finance API.
    Fill in your cookies, headers and params here.
    """
    headers = {
        'cookie': os.getenv('YAHOO_COOKIE'),
        'user-agent': os.getenv('USER_AGENT'),
    }

    common_params = {
        'crumb': os.getenv('CRUMB'),  # security token for defensing CSRF attack, optional
        'lang': 'en-US',
        'region': 'US',
        'formatted': 'true',
        'corsDomain': 'finance.yahoo.com',
    }

    common_payload_data = {
        'offset': 0,  # The offset is the number of items to skip before starting to collect the items.
        'size': 25,  # The size (also known as limit or pageSize) is the maximum number of items to return in a single page.
        'sortType': 'DESC',
        'sortField': 'intradaymarketcap',
        'quoteType': 'CRYPTOCURRENCY',
        'query': {
            'operator': 'and',
            'operands': [
                {
                    'operator': 'eq',
                    'operands': [
                        'currency',
                        'USD',
                    ],
                },
                {
                    'operator': 'eq',
                    'operands': [
                        'exchange',
                        'CCC',
                    ],
                },
            ],
        },
        'userId': '',
        'userIdType': 'guid',
    }

    return common_params, headers, common_payload_data
