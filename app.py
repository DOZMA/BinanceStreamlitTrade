import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from binance.client import Client
import time
import datetime as dt
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Inicialização do cliente Binance com credenciais seguras
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = Client(api_key, api_secret)

# Configurações de e-mail para alertas
email_user = os.getenv("EMAIL_USER")
email_password = os.getenv("EMAIL_PASSWORD")

# Função para enviar e-mail de alerta
def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = email_user
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_user, email_password)
        server.sendmail(email_user, email_user, msg.as_string())

# Sidebar para configurações do usuário
st.sidebar.title("Configurações")
crypto_symbol = st.sidebar.selectbox("Selecione a criptomoeda", options=["BTCUSDT", "ETHUSDT", "BNBUSDT"])
interval = st.sidebar.selectbox("Intervalo de tempo", options=["1m", "3m", "5m", "15m", "30m", "1h", "4h"])
lookback_period = st.sidebar.text_input("Período de análise (ex: '30m', '1h')", value="30m")
stop_loss = st.sidebar.number_input("Stop Loss (%)", min_value=0.0, max_value=100.0, value=0.5)
take_profit = st.sidebar.number_input("Take Profit (%)", min_value=0.0, max_value=100.0, value=1.5)

# Função para obter dados históricos
def get_data(symbol, interval, lookback):
    klines = client.get_historical_klines(symbol, interval, lookback)
    df = pd.DataFrame(klines)
    df = df.iloc[:, :6]
    df.columns = ['date_open', 'Open', 'High', 'Low', 'Close', 'Volume']
    df['date_open'] = pd.to_datetime(df['date_open'], unit='ms')
    df.set_index('date_open', inplace=True)
    df = df.astype(float)
    return df

# Função de análise para determinar sugestões de compra/venda/manter
def analyze_data(df):
    retorno_acum = (df['Open'].pct_change() + 1).cumprod() - 1
    if retorno_acum.iloc[-1] < -stop_loss / 100:
        return "Comprar", "green"
    elif retorno_acum.iloc[-1] > take_profit / 100:
        return "Vender", "red"
    else:
        return "Manter", "yellow"

# Exibir dados e sugestão
st.title(f"Análise de {crypto_symbol}")
st.write("Obtendo dados...")
df = get_data(crypto_symbol, interval, lookback_period)
st.line_chart(df['Close'])

# Sugestão de ação
acao, cor = analyze_data(df)
st.markdown(f"<h3 style='color:{cor}'>Sugestão: {acao}</h3>", unsafe_allow_html=True)

# Botões de ação
st.write("### Executar Ordens")
if st.button("Comprar"):
    st.write("Executando ordem de compra...")  
    # client.order_market_buy(symbol=crypto_symbol, quantity=0.001)
    st.success("Ordem de compra executada!")
    send_email("Alerta: Ordem de Compra Executada", f"Comprado {crypto_symbol} às {dt.datetime.now()}")

if st.button("Vender"):
    st.write("Executando ordem de venda...")
    # client.order_market_sell(symbol=crypto_symbol, quantity=0.001)
    st.success("Ordem de venda executada!")
    send_email("Alerta: Ordem de Venda Executada", f"Vendido {crypto_symbol} às {dt.datetime.now()}")

# Log de operações
log_df = pd.DataFrame(columns=['Data', 'Ação', 'Cripto', 'Preço'])

def log_operation(action, price):
    global log_df
    new_log = pd.DataFrame([[dt.datetime.now(), action, crypto_symbol, price]], 
                           columns=['Data', 'Ação', 'Cripto', 'Preço'])
    log_df = pd.concat([log_df, new_log], ignore_index=True)
    log_df.to_csv("log_operacoes.csv", index=False)

# Atualização automática
auto_refresh = st.sidebar.checkbox("Atualizar automaticamente a cada 30 segundos")

if auto_refresh:
    st.experimental_rerun()  # Força uma atualização da página.
