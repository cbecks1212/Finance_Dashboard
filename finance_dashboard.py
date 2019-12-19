#import modules
from datetime import datetime
from iexfinance.stocks import get_historical_data
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#declare date range
start = datetime(2019, 1, 1)
end = datetime.today()

#get ticker data
ticker_df = pd.read_csv('ticker_data.csv')
tickers = ticker_df.Symbol.values.tolist()


st.title('Finance Portal')
#create sidebar with options
sidebar = st.sidebar.selectbox('Select an Option',['Stocks', 'Crypto', 'Fixed Income'])

#Stock Page
if sidebar == 'Stocks':
    dropdown = st.selectbox('Select a Ticker', tickers)
    df = get_historical_data(dropdown, start, end, output_format='pandas', token='YOUR API KEY')
    fig = px.line(df, x=df.index, y=df.close, title=str(dropdown)+' 2019 Performance')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Stock Price')
    st.plotly_chart(fig)
    first_value = df.close.iloc[0]
    last_value = df.close.iloc[-1]
    change = (last_value - first_value)/first_value
    st.write(change)

#Fixed Income Page
elif sidebar == 'Fixed Income':
    radio_options = st.radio("Treasury Option", ['2-Year', '5-Year', 'Both'])
    df_2yr = pd.read_csv('DGS2.csv')
    df_5yr = pd.read_csv('DGS5.csv')
    if radio_options == '2-Year':
        fig = px.line(x=df_2yr.DATE, y=df_2yr.DGS2, title='2-Year Treasury')
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Yield')
        st.plotly_chart(fig)
    elif radio_options == '5-Year':
        fig = px.line(x=df_5yr.DATE, y=df_5yr.DGS5, title='5-Year Treasury')
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Yield')
        st.plotly_chart(fig)
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_2yr.DATE, y=df_2yr.DGS2, mode='lines', name='2-Year'))
        fig.add_trace(go.Scatter(x=df_5yr.DATE, y=df_5yr.DGS5, mode='lines', name='5-Year'))
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Yield')
        st.plotly_chart(fig)

#Crypto Page
elif sidebar == 'Crypto':
    #compare Bitcoin to any stock
    dropdown = st.selectbox('Select a Ticker', tickers)
    checkbox = st.checkbox('Click for Results')
    stock_df = get_historical_data(dropdown, start, end, output_format='pandas', token='sk_0d614da79c6f4f1aa708c54d9a699d01')
    crypto_df = pd.read_csv('BTC_USD_2018-12-15_2019-12-14-CoinDesk.csv')
    bar_list = ['Asset Performance']
    #crypto_df = crypto_df.query('Date >=2019-01-01')
    if checkbox:
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df.close, mode='lines', name=dropdown),secondary_y=True)
        fig.add_trace(go.Scatter(x=crypto_df.Date, y=crypto_df['Closing Price (USD)'], mode='lines', name='Bitcoin'),secondary_y=False)
        fig.update_xaxes(title='Date')
        # Set y-axes titles
        fig.update_yaxes(title_text="Stock Price", secondary_y=True)
        fig.update_yaxes(title_text="Bitcoin Price", secondary_y=False)
        st.plotly_chart(fig)
        #Calculate Percentage change
        first = crypto_df['Closing Price (USD)'].iloc[0]
        last = crypto_df['Closing Price (USD)'].iloc[-1]
        btc_change = ((last-first)/first)*100
        stock_first = stock_df.close.iloc[0]
        stock_last = stock_df.close.iloc[-1]
        stock_change = ((stock_last-stock_first)/stock_first)*100
        btc_change_s = pd.Series(data=btc_change)
        stock_change_s = pd.Series(data=stock_change)
        #graph two changes
        bar_fig = go.Figure(data=[
            go.Bar(name=dropdown, x=bar_list, y=stock_change_s),
            go.Bar(name='Bitcoin', x=bar_list, y=btc_change_s)
        ])
        bar_fig.update_layout(barmode='group')
        bar_fig.update_layout(title_text='BTC vs ' + dropdown)
        st.plotly_chart(bar_fig)
