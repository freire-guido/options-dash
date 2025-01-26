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
data['daysFromToday'] = (data['expirationDate'] - datetime.today()).dt.days
data['optionType'] = data['symbol'].str.extract(r'-([CP])$')[0]

st.sidebar.header("Filter by Expiration Date")
days_from_today = st.sidebar.slider(
    "Days from Today",
    min_value=1,
    max_value=7,
    value=1,
    help="Filter options by expiration date (number of days from today)"
)

filtered = data[data['daysFromToday'] == days_from_today - 1]
filtered = filtered[(filtered['bidPrice'] > 50) & (filtered['askPrice'] > 50)]

calls = filtered[filtered['optionType'] == 'C']
puts = filtered[filtered['optionType'] == 'P']
calls = calls.sort_values(by='strikePrice')
puts = puts.sort_values(by='strikePrice')

st.title("Binance Options Dashboard")
st.subheader("BTC Options: Strike Price vs. Option Price")

fig = px.line()

# Add bid/ask for calls (dashed lines)
fig.add_scatter(x=calls['strikePrice'], y=calls['bidPrice'], mode='lines', name='Call Bid', 
                line=dict(dash='dash', color='green'))  # Green for bid
fig.add_scatter(x=calls['strikePrice'], y=calls['askPrice'], mode='lines', name='Call Ask', 
                line=dict(dash='dash', color='red'))  # Red for ask

# Add bid/ask for puts (solid lines)
fig.add_scatter(x=puts['strikePrice'], y=puts['bidPrice'], mode='lines', name='Put Bid', 
                line=dict(color='green'))  # Green for bid
fig.add_scatter(x=puts['strikePrice'], y=puts['askPrice'], mode='lines', name='Put Ask', 
                line=dict(color='red'))  # Red for ask

# Update layout
fig.update_layout(
    xaxis_title="Strike Price",
    yaxis_title="Option Price",
    title="Strike Price vs. Option Price",
    legend_title="Price Type"
)

st.plotly_chart(fig)
st.subheader("Raw Data")
st.write(filtered)