import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from datetime import datetime
from options import fetch_binance_options

data = fetch_binance_options()
data = data[data['symbol'].str.contains('BTC')]
data['expirationDate'] = data['symbol'].str.extract(r'-(\d{6})-')[0]
data['expirationDate'] = pd.to_datetime(data['expirationDate'], format='%y%m%d')

st.sidebar.header("Filter by Expiration Date")
days_from_today = st.sidebar.slider(
    "Days from Today",
    min_value=0,
    max_value=31,
    value=0,
    help="Filter options by expiration date (number of days from today)"
)

data['daysFromToday'] =  (data['expirationDate'] - datetime.today()).dt.days
filtered = data[data['daysFromToday'] == days_from_today]

st.title("Binance Options Dashboard")
st.subheader("BTC Put Options: Strike Price vs. Option Price")
fig = px.line(filtered, x='strikePrice', y=['bidPrice', 'askPrice'],
              labels={'value': 'Option Price', 'variable': 'Price Type'},
              title="Strike Price vs. Option Price")
st.plotly_chart(fig)

st.subheader("Raw Data")
st.write(data)