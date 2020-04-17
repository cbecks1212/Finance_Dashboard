import pandas as pd
import lxml
import streamlit as st
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from pandas.io.json import json_normalize
import yfinance as yf
import requests
import base64
os.chdir('/Users/curtbeck/downloads')
stock_df = pd.read_csv('SP_data.csv')

def get_tickers():
    nasdaq_web = requests.get('https://www.stockmonitor.com/nasdaq-stocks/')
    nasdaq_data = nasdaq_web.content
    df = pd.read_html(nasdaq_data)
    return df[0]

def retrieve_data():
    data = yf.Ticker(tickers)
    df = data.history(start=start, end=end)
    #df = get_historical_data(symbols=tickers, token='pk_d2898c0938b043c0957d66b5953c142d', output_format='pandas', start=start, end=end)
    fig = px.line(df, x=df.index, y=df.Close, title=str(tickers)+ ' Stock Performance')
    st.plotly_chart(fig)
    return df

def get_stats():
    web_data = requests.get('https://finance.yahoo.com/quote/' + tickers + '/key-statistics?p=' + tickers)
    content = web_data.content
    df = pd.read_html(content)
    df = df[1]
    st.write(df)

def balance_sheet():
    web_data = requests.get('https://finance.yahoo.com/quote/' + tickers + '/key-statistics?p=' + tickers)
    content = web_data.content
    df = pd.read_html(content)
    df = df[8]
    st.write(df)

def valuations():
    web_data = requests.get('https://finance.yahoo.com/quote/' + tickers + '/key-statistics?p=' + tickers)
    content = web_data.content
    df = pd.read_html(content)
    df = df[0]
    st.write(df)

def download_data(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download Raw Data</a>'
    return href

#create dashboard--sidebar
st.sidebar.subheader("""Welcome to the Stock Portal:
Quickly assess the Performance of a Stock.""")

index = st.sidebar.radio(label='Index', options=['S&P 500', 'Nasdaq', 'Search for a Ticker'])
start = st.sidebar.date_input(label='Start')
end = st.sidebar.date_input(label='End')
if index == 'S&P 500':
    tickers = st.sidebar.selectbox(label='Ticker', options=stock_df['Symbol'])
    if tickers:
        df= retrieve_data()
        st.markdown(download_data(df), unsafe_allow_html=True)
        st.subheader(tickers + '\'s' + " Ratios Over the Past Year")
        stats = get_stats()
        st.subheader(tickers + '\'s' + " Balance Sheet:")
        balance_sheet = balance_sheet()
        st.subheader(tickers + '\'s' + " Valuation Measures:")
        valuations = valuations()

elif index == 'Search for a Ticker':
    tickers = st.sidebar.text_input(label='Enter a Ticker')
    if tickers:
        df = retrieve_data()
        st.markdown(download_data(df), unsafe_allow_html=True)
        st.subheader(tickers + '\'s' + " Stock Price History:")
        stats = get_stats()
        st.subheader(tickers + '\'s' + " Balance Sheet:")
        balance_sheet = balance_sheet()
        st.subheader(tickers + '\'s' + " Valuation Measures:")
        valuations = valuations()
    
else:
    nasdaq_df = get_tickers()
    tickers = st.sidebar.selectbox(label='Ticker', options = nasdaq_df['Company'])
    if tickers:
        fig = retrieve_data()
        st.subheader(tickers + '\'s' + " Stock Price History")
        stats = get_stats()
        st.subheader(tickers + '\'s' + " Balance Sheet:")
        balance_sheet = balance_sheet()
        st.subheader(tickers + '\'s' + " Valuation Measures:")


