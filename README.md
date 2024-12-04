# Crypto Trading Bot with Streamlit
## Overview
This project is a crypto trading bot that interacts with the Binance API using a Streamlit web interface. The app provides real-time analysis of cryptocurrency price data and offers buy/sell recommendations based on user-defined criteria such as stop loss and take profit thresholds. Users can also manually execute market orders directly from the interface.

## Key Features
### Real-time Data Fetching:
Retrieves historical price data for various cryptocurrencies (e.g., BTC, ETH) from Binance.

## Buy/Sell Recommendations:
### Offers actionable insights using color-coded suggestions:
 - 🟢 Buy: Green indicates a buy opportunity.
 - 🔴 Sell: Red suggests selling the asset.
 - 🟡 Hold: Yellow signals holding the current position.
  
## Manual Order Execution:
Execute market buy or market sell orders directly through the interface.
Logs each transaction for future reference.

## ARisk Management:
Users can configure Stop Loss and Take Profit thresholds via a sidebar for controlled risk exposure.

## Email Alerts:
Sends email notifications when buy or sell orders are executed.

## Auto-refresh Feature:
Option to automatically refresh the data and analysis every 30 seconds for continuous monitoring.

## Secure Credentials Handling:
API keys and email credentials are securely stored in a secrets.toml file.
