import requests
import pandas as pd

def fetch_binance_options():
    url = "https://eapi.binance.com/eapi/v1/ticker"
    response = requests.get(url)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)