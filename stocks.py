from rich.console import Console
from rich.table import Table
import requests
from requests.models import Response
import os
from typing import Dict, Any, List

# connect to https://www.alphavantage.co/query API
BASE_URL: str = "https://www.alphavantage.co/query"
KEY: str = str(os.getenv("ALPHA_KEY"))


def endpoint(base_url: str, key: str, symbol: str, series_func: str, **kwargs) -> dict:
    """
    wrapper to get stock data from endpoint

    Args:
        base_url: base url to alphaavantage api
        key:  private key to access alphaavantage api
        symbol: stock symbol to get data on
        series_fuc: series of data wanted. see api documentation
        **kwargs: aditional arguments based on api documentation
    """
    required_params: Dict[str, str] = {"function": series_func, "symbol": symbol}
    optional_params: Dict[str, str] = kwargs
    payload: Dict[str, str] = {**required_params, **optional_params, "apikey": key}
    r: Response = requests.get(base_url, params=payload)
    data: Dict[str, Dict[str, str]] = r.json()
    return data


def get_series_name(stock_data: Dict[str, Dict[str, str]]) -> str:
    """
    get the name of the series of data returned

    Args:
    stock_data: a dict data structure from the endpoint function

    """
    series_name: str = [series for series in stock_data if series != "Meta Data"][0]
    return series_name


def get_table_headers(stock_data: Dict[str, Dict[str, str]], series_name: str) -> list:
    """
    get the table header names

    Args:
    stock_data: dict data structure from the endpoint function
    series_name: internal api name of series


    """
    first_value: str = list(stock_data[series_name].keys())[0]
    table_headers: List[str] = list(stock_data[series_name][first_value].keys())
    return table_headers


def build_table(stock_data: Dict[str, Dict[str, str]], series_name: str) -> Table:
    table: Table = Table(title=stock_data["Meta Data"]["1. Information"])
    table.add_column("date")
    [table.add_column(headers) for headers in table_headers]  # type: ignore[func-returns-value]

    for k, v in stock_data[series_name].items():
        name: list = [k]
        values: list = list(v.values())
        row: list = name + values
        table.add_row(*row)
    return table


stock_data: Dict[str, Dict[str, str]] = endpoint(
    BASE_URL, KEY, "IBM", "TIME_SERIES_MONTHLY"
)

series_name = get_series_name(stock_data)
table_headers = get_table_headers(stock_data, series_name)
table = build_table(stock_data, series_name)


console = Console()
console.print(table)
