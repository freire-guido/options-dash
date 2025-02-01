import requests
import pandas as pd

def fetch_binance_options(symbol = None):
    url = "https://eapi.binance.com/eapi/v1/ticker"
    response = requests.get(url, params = {"symbol": symbol})
    response.raise_for_status()
    if response.status_code == 200:
        data = pd.DataFrame(response.json())
        data['bidPrice'] = data['bidPrice'].astype(float)
        data['askPrice'] = data['askPrice'].astype(float)
        data['strikePrice'] = data['strikePrice'].astype(float)
        data['amount'] = data['amount'].astype(float)
        data['volume'] = data['volume'].astype(float)
        data['exercisePrice'] = data['exercisePrice'].astype(float)
        return data
    
def fetch_mark_price(symbol = None):
    url = "https://eapi.binance.com/eapi/v1/mark"
    response = requests.get(url, params= {"symbol": symbol})
    response.raise_for_status()
    if response.status_code == 200:
        data = pd.DataFrame(response.json())
        data['markPrice'] = data['markPrice'].astype(float)
        return data