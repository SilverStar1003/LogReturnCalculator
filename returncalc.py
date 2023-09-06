import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title('📈 Log Return Calculator')
st.write("The LogReturnCalculator is a web application designed to provide users with the ability to input stock symbols and timeframes, and generate and visualize log returns for the specified stocks")
# Get user input for stock ticker symbol

st.markdown("<hr>", unsafe_allow_html=True)
st.header('🔍Market Data Retrieval and Logarithmic Return Calculation')
st.markdown("<hr>", unsafe_allow_html=True)
ticker = st.text_input("Enter stock ticker symbol (e.g., AAPL):")

# Define timeframe options
timeframes = {
    "5D": 5,
    "10D": 10,
    "1M": 30,
    "3M": 90,
    "6M": 180,
    "YTD": "YTD"
}

# Get user input for timeframe selection
selected_timeframe = st.selectbox("Select a timeframe:", list(timeframes.keys()))

# Placeholder for stock data and log returns
stock_data = None
log_returns = None


# Define function to retrieve stock data
@st.cache_data(ttl=60 * 5)  # Caches the data for 5 minutes to avoid redundant API calls
def load_stock_data(ticker, timeframe):
    try:
        if isinstance(timeframe, int):
            data = yf.download(ticker, period=f"{timeframe}d")
        else:
            data = yf.download(ticker, period=timeframe)
        return data
    except Exception as e:
        st.error("Error retrieving stock data. Please check your inputs.")
        st.stop()


# Retrieve stock data and calculate log returns
if st.button("Calculate"):
    stock_data = load_stock_data(ticker, timeframes[selected_timeframe])

    # Check if stock data is empty or contains valid records
    if stock_data.empty or stock_data['Close'].isnull().all():
        st.error("No data available for the specified stock ticker and timeframe.")
    else:
        # Calculate logarithmic returns using adjusted close prices
        log_returns = np.log(stock_data['Close'] / stock_data['Close'].shift(1))

# Display the stock data and log returns
if stock_data is not None:
    st.subheader("Stock Data")
    stock_data = stock_data.iloc[::-1]
    st.dataframe(stock_data)

    col1, col2 = st.columns(2)
    # Plot log returns using seaborn
    with col1:
        sns.set_style("darkgrid")
        fig, ax = plt.subplots()
        sns.lineplot(data=log_returns, ax=ax)
        st.pyplot(fig)

    # Display the log returns table
    with col2:
        st.subheader("Log Returns")
        log_returns = log_returns.iloc[::-1]
        st.dataframe(log_returns)
