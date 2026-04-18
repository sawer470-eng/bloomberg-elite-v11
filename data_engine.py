import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import time

@st.cache_data(ttl=3600)
def fetch_ticker_data(ticker, fallback_google_ticker=None):
    """
    Syndicate fetching: Try yfinance -> Google Finance -> Finviz
    """
    # 1. Try yfinance
    try:
        asset = yf.Ticker(ticker)
        hist = asset.history(period="1mo")
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            if any(x in ticker for x in ['^TNX', '^IRX', '^TYX', '^FVX']):
                price = price / 10.0
            last_close = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else last_close
            change = (last_close - prev_close) / (10.0 if any(x in ticker for x in ['^TNX', '^IRX', '^TYX', '^FVX']) else 1.0)
            pct_change = (change / (prev_close / (10.0 if any(x in ticker for x in ['^TNX', '^IRX', '^TYX', '^FVX']) else 1.0))) * 100 if prev_close != 0 else 0
            
            return {
                "price": price,
                "change": change,
                "pct_change": pct_change,
                "history": hist['Close'] / (10.0 if any(x in ticker for x in ['^TNX', '^IRX', '^TYX', '^FVX']) else 1.0),
                "source": "Yahoo"
            }
    except:
        pass

    # 2. Try Google Finance
    if fallback_google_ticker:
        try:
            url = f"https://www.google.com/finance/quote/{fallback_google_ticker}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            price_el = soup.select_one('.YMlKec.fxKbKc')
            if price_el:
                price = float(price_el.text.replace('$', '').replace(',', '').strip())
                return {"price": price, "change": 0.0, "pct_change": 0.0, "history": pd.Series([price]*20), "source": "Google"}
        except:
            pass

    # 3. Try Finviz (Deep Fallback)
    try:
        cleaned_ticker = ticker.replace('^', '').replace('=X', '')
        url = f"https://finviz.com/quote.ashx?t={cleaned_ticker}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/4.0"}, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_el = soup.select_one('.quote-price_grid') or soup.find(id="price")
        if price_el:
            price = float(price_el.text.strip())
            return {"price": price, "change": 0.0, "pct_change": 0.0, "history": pd.Series([price]*20), "source": "Finviz"}
    except:
        pass

    return {"price": 0.0, "change": 0.0, "pct_change": 0.0, "history": pd.Series([0.0]*5), "source": "N/A", "is_failed": True}

@st.cache_data(ttl=3600)
def fetch_macro_yields():
    tickers = {
        "10Y Yield": ("^TNX", "TNX:INDEXCBOE"),
        "2Y Yield": ("^IRX", "IRX:INDEXCBOE"),
        "30Y Yield": ("^TYX", "TYX:INDEXCBOE")
    }
    
    results = {}
    for name, (yf_tkr, go_tkr) in tickers.items():
        data = fetch_ticker_data(yf_tkr, go_tkr)
        results[name] = data
    return results

def get_ticker_tape_data():
    symbols = {
        "S&P 500": ("^GSPC", "SPY:NYSE"),
        "NASDAQ": ("^NDX", "QQQ:NASDAQ"),
        "GOLD": ("GC=F", "GOLD:COMEX"),
        "CRUDE": ("CL=F", "CL.1:COMEX"),
        "BTC": ("BTC-USD", "BTC-USD")
    }
    
    items = []
    for name, (yf_tkr, go_tkr) in symbols.items():
        data = fetch_ticker_data(yf_tkr, fallback_google_ticker=go_tkr)
        if data and not data.get('is_failed'):
            color = "#66ff00" if data['pct_change'] >= 0 else "#ff0033"
            arrow = "▲" if data['pct_change'] >= 0 else "▼"
            items.append(f"<span style='color:#c5c6c7'>{name}</span> <span style='color:{color}'>{data['price']:,.2f} {arrow} {abs(data['pct_change']):.2f}%</span>")
        else:
            items.append(f"<span style='color:#c5c6c7'>{name}</span> <span style='color:#8b949e'>N/A</span>")
            
    return " &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; ".join(items)
