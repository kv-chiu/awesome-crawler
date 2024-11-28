# -*- coding: utf-8 -*-
# @Author  : kelvin.chiu021@gmail.com
# @Time    : 2024/11/28 13:28
# @Desc    : Test Yahoo Finance Crypto API Request

import pprint

import requests


cookies = {
    # fill in your cookies here
}

headers = {
    # fill in your headers here
}

params = {
    # fill in your params here
}

response = requests.get(
    'https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved',
    params=params,
    cookies=cookies,
    headers=headers,
)


if __name__ == '__main__':
    pprint.pprint(response.json())
