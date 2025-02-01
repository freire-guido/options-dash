import streamlit as st
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datetime import datetime
from options import fetch_binance_options, fetch_mark_price

symbol = 'BTC'

st.sidebar.header("Filter by Expiration Date")
days_from_today = st.sidebar.slider(
    "Days from Today",
    min_value=1,
    max_value=7,
    value=1,
    help="Filter options by expiration date (number of days from today)"
)

options = fetch_binance_options()
marks = fetch_mark_price()

options = options[options['symbol'].str.contains(symbol)]
data = options.join(marks.set_index('symbol'), on='symbol')

data['expirationDate'] = data['symbol'].str.extract(r'-(\d{6})-')[0]
data['expirationDate'] = pd.to_datetime(data['expirationDate'], format='%y%m%d')
data['daysFromToday'] = (data['expirationDate'] - datetime.today()).dt.days
data['optionType'] = data['symbol'].str.extract(r'-([CP])$')[0]

filtered = data[data['daysFromToday'] == days_from_today - 1]
filtered = filtered[(filtered['bidPrice'] > 50) & (filtered['askPrice'] > 50)]

calls = filtered[filtered['optionType'] == 'C']
puts = filtered[filtered['optionType'] == 'P']
calls = calls.sort_values(by='strikePrice')
puts = puts.sort_values(by='strikePrice')

st.title("Binance Options Dashboard")
st.subheader("$BTC")

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.1,
    row_heights=[0.7, 0.3]
)

# Add bid/ask for calls (dashed lines)
fig.add_trace(go.Scatter(
        x=calls['strikePrice'],
        y=calls['bidPrice'],
        mode='lines',
        name='Call Bid',
        line=dict(dash='dash', color='green')), # Green for bid
    row=1, col=1
)
fig.add_trace(go.Scatter(
        x=calls['strikePrice'],
        y=calls['askPrice'],
        mode='lines',
        name='Call Ask',
        line=dict(dash='dash', color='red')),   # Red for ask
    row=1, col=1
)

# Add bid/ask for puts (solid lines)
fig.add_trace(go.Scatter(
        x=puts['strikePrice'],
        y=puts['bidPrice'],
        mode='lines',
        name='Put Bid',
        line=dict(color='green')),  # Green for bid
    row=1, col=1
)
fig.add_trace(go.Scatter(
        x=puts['strikePrice'],
        y=puts['askPrice'],
        mode='lines',
        name='Put Ask',
        line=dict(color='red')),    # Red for ask
    row=1, col=1
)

# Add a vertical line at the exercisePrice (current price)
if not filtered.empty:
    exercise_price = filtered['exercisePrice'].iloc[0]  # Assuming exercisePrice is the same for all rows
    fig.add_vline(
        x=exercise_price, line_dash="dot", line_color="blue", 
        annotation_text=f"Current: {int(exercise_price)}", 
        annotation_position="top right",
        row=1, col=1
    )

# Add histogram for amount
fig.add_trace(
    go.Histogram(x=filtered['strikePrice'], y=filtered['amount'], name='Amount'),
    row=2,
    col=1
)

# Update layout
fig.update_layout(
    yaxis_title="Option Price",
    legend_title="Price Type",
)

st.plotly_chart(fig)
st.subheader("Raw Data")
st.write(filtered)