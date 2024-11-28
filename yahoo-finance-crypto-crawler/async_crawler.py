# -*- coding: utf-8 -*-
# @Author  : kelvin.chiu021@gmail.com
# @Time    : 2024/11/28 14:54
# @Desc    : Asynchronous Yahoo Finance Crypto API Crawler

import asyncio
import csv
import random
import time
from typing import Any, Dict, List

import aiofiles
import httpx

from common import SymbolContent, request_params_and_headers_factory

HOST = "https://query1.finance.yahoo.com"
SYMBOL_QUERY_API_URI = "/v1/finance/screener"
PAGE_SIZE = 100  # alternatives: 25, 50, 100


def parse_symbol_content(quote_item: Dict) -> SymbolContent:
    """
    Parse symbol content from quote item.
    :param quote_item:
    :return:
    """
    symbol_content = SymbolContent()
    symbol_content.symbol = quote_item["symbol"]
    symbol_content.name = quote_item["shortName"]
    symbol_content.price = quote_item["regularMarketPrice"]["fmt"]
    symbol_content.change_price = quote_item["regularMarketChange"]["fmt"]
    symbol_content.change_percent = quote_item["regularMarketChangePercent"]["fmt"]
    symbol_content.market_price = quote_item["marketCap"]["fmt"]
    return symbol_content


async def fetch_currency_data_list(max_total_count: int) -> List[SymbolContent]:
    """
    Fetch currency data list.
    :param max_total_count:
    :return:
    """
    symbol_data_list: List[SymbolContent] = []
    page_start = 0
    while page_start <= max_total_count:
        response_dict: Dict = await send_request(page_start=page_start, page_size=PAGE_SIZE)
        for quote in response_dict["finance"]["result"][0]["quotes"]:
            parsed_content: SymbolContent = parse_symbol_content(quote)
            print(parsed_content)
            symbol_data_list.append(parsed_content)
        page_start += PAGE_SIZE
        await asyncio.sleep(random.random())
    return symbol_data_list


async def send_request(page_start: int, page_size: int) -> Dict[str, Any]:
    """
    Send request to Yahoo Finance API.
    :param page_start: Offset
    :param page_size: Size
    :return:
    """
    print(f"[send_request] page_start:{page_start}")
    req_url = HOST + SYMBOL_QUERY_API_URI
    common_params, headers, common_payload_data = request_params_and_headers_factory()
    # 修改分页变动参数
    common_payload_data["offset"] = page_start
    common_payload_data["size"] = page_size

    async with httpx.AsyncClient() as client:
        response = await client.post(url=req_url, params=common_params, json=common_payload_data, headers=headers,
                                     timeout=30)
    if response.status_code != 200:
        raise Exception("An error occurred with the request, reason:", response.text)
    try:
        response_dict: Dict = response.json()
        return response_dict
    except Exception as e:
        raise e


async def get_max_total_count() -> int:
    """
    Get the maximum number of currencies.
    :return:
    """
    print("Start getting the maximum number of coins")
    try:
        response_dict: Dict = await send_request(page_start=0, page_size=PAGE_SIZE)
        total_num: int = response_dict["finance"]["result"][0]["total"]
        print(f"Get {total_num} coins.")
        return total_num
    except Exception as e:
        print("Error occurred when getting the maximum number of coins, reason:", e)
        return 0


async def save_data_to_csv(save_file_name: str, currency_data_list: List[SymbolContent]) -> None:
    """
    Save data to CSV.
    :param save_file_name: Save file name
    :param currency_data_list:
    :return:
    """
    async with aiofiles.open(save_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header of the CSV file
        await writer.writerow(SymbolContent.get_fields())

        # Write all symbol data to the CSV file
        for symbol in currency_data_list:
            await writer.writerow([symbol.symbol, symbol.name, symbol.price, symbol.change_price, symbol.change_percent,
                                   symbol.market_price])


async def run_crawler(save_file_name: str) -> None:
    """
    Run crawler.
    :param save_file_name:
    :return:
    """
    # step1: Get the maximum number of currencies
    max_total: int = await get_max_total_count()
    # step2: Fetch currency data list
    data_list: List[SymbolContent] = await fetch_currency_data_list(max_total)
    # step3: Save data to CSV
    await save_data_to_csv(save_file_name, data_list)


if __name__ == '__main__':
    timestamp = int(time.time())
    save_csv_file_name = f"symbol_data_{timestamp}.csv"
    asyncio.run(run_crawler(save_csv_file_name))
