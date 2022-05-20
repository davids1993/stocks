from rich.console import Console
from rich.table import Table
import requests

# connect to https://www.alphavantage.co/query API
BASE_URL = 'https://www.alphavantage.co/query'
KEY = 'KC7GR4DRG5HSNUEJ'


def endpoint(base_url:str, key:str, symbol:str, series_func:str, **kwargs) -> dict:
    """
    wrapper to get stock data from endpoint
    
    Args:
        base_url: base url to alphaavantage api
        key:  private key to access alphaavantage api
        symbol: stock symbol to get data on
        series_fuc: series of data wanted. see api documentation
        **kwargs: aditional arguments based on api documentation
    """
    required_params = {'function': series_func, 'symbol':symbol}
    optional_params = kwargs
    payload = {**required_params, **optional_params, 'apikey':key}
    r = requests.get(base_url, params=payload)
    data = r.json()
    return data
    
    
stock_data = endpoint(BASE_URL, KEY, 'IBM', 'TIME_SERIES_MONTHLY')

series_key = [series for series in stock_data if series != 'Meta Data'][0]

table = Table(title=stock_data['Meta Data']['1. Information'])

first_value = list(stock_data[series_key].keys())[0]

columns = stock_data[series_key][first_value]
columns = list(columns.keys())

table.add_column('date')
[table.add_column(column) for column in columns]

for k, v in stock_data[series_key].items():
    name = [k]
    values = list(v.values())
    row = name + values
    table.add_row(*row)
    



console = Console()
console.print(table)









    
    
    
    

