import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup

@st.cache
def tickers_sp500():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.rstrip()
        tickers.append(ticker)
    return tickers

# Set page title and icon
st.set_page_config(page_title='S&P 500 Stock Price App', page_icon=':chart_with_upwards_trend:')
st.title('Stock Price App')

# Set sidebar title
st.sidebar.header('Input Parameters')

# Get the list of all S&P500 tickers
all_tickers = yf.Tickers(tickers_sp500())

# Get the list of all ticker symbols
tickers_list = all_tickers.tickers

# Define ticker input
ticker = st.sidebar.selectbox('Select Ticker', tickers_list)

# Define date range input with default value as today's date
start_date = st.sidebar.date_input('Start Date', value=dt.date.today())
end_date = st.sidebar.date_input('End Date', value=dt.date.today())

# Get the stock data for the selected ticker and date range
ticker_data = yf.Ticker(ticker)
ticker_df = ticker_data.history(start=start_date, end=end_date)

# Define metrics to display
metrics = st.sidebar.multiselect('Select Metrics', ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'], default=['Close', 'Volume'])

try:
    ticker_data = yf.Ticker(ticker)
    ticker_df = ticker_data.history(period='1d', start=start_date, end=end_date)
except:
    st.error(f"No data available for {ticker}")

# Display the selected metrics
for metric in metrics:
    if metric == 'Volume':
        st.write(f"## Volume for {ticker}")
        st.line_chart(ticker_df[metric])
    else:
        st.write(f"## {metric} for {ticker}")
        st.line_chart(ticker_df[metric])

# Add a moving average chart
if 'Close' in metrics:
    ma_period = st.sidebar.slider('Moving Average Period', 2, 50, 20)
    ma = ticker_df['Close'].rolling(ma_period).mean()
    st.write(f"## Moving Average Chart for {ticker}")
    st.line_chart(ma)

# Add a candlestick chart
if {'Open', 'High', 'Low', 'Close'}.issubset(metrics):
    fig = go.Figure(data=[go.Candlestick(x=ticker_df.index,
                                         open=ticker_df['Open'],
                                         high=ticker_df['High'],
                                         low=ticker_df['Low'],
                                         close=ticker_df['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

# Add a table of data
st.write(f"## {ticker} Data")
st.dataframe(ticker_df[metrics])