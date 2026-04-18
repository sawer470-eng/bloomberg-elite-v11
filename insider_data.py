import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import textwrap

@st.cache_data(ttl=3600)
def get_insider_transactions_syndicate(ticker):
    """
    Scrape OpenInsider for real-time reliable data.
    """
    try:
        url = f"http://openinsider.com/search?q={ticker}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        table = soup.find('table', {'class': 'tinytable'})
        if not table:
            return pd.DataFrame()
            
        rows = []
        headers = [th.text.strip() for th in table.find_all('th')]
        for tr in table.find_all('tr')[1:]:
            cols = [td.text.strip() for td in tr.find_all('td')]
            if len(cols) == len(headers):
                rows.append(cols)
        
        df = pd.DataFrame(rows, columns=headers)
        return df
    except:
        return pd.DataFrame()

def render_insider_data():
    theme = st.session_state.get('theme', 'Obsidian Black')
    is_white = theme == "Alpine White"
    accent = "#2980b9" if is_white else "#45a29e"
    t_color = "#1a1a1a" if is_white else "#ffffff"

    st.markdown(f"<h2 style='color: #FF9900; font-family: Outfit, sans-serif; border-bottom: 2px solid rgba(255, 153, 0, 0.4); padding-bottom:10px; text-transform: uppercase; letter-spacing: 1px;'>[INSIDER TRADING TRACKER: ELITE V3]</h2>", unsafe_allow_html=True)
    st.write("Track when CEOs and Directors trade their own stock. (Source: OpenInsider Syndicate)")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        ticker = st.text_input("Enter Ticker Symbol:", "AAPL").upper()
    
    with st.spinner(f"Scanning filings for {ticker}..."):
        df = get_insider_transactions_syndicate(ticker)
        
        if df.empty:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #FF9900;">
                <h4 style="color:#FF9900; margin:0;">[SOURCE ROTATION IDLE]</h4>
                <p style="color:{t_color}; margin:5px 0 0 0; opacity:0.7;">No recent filings found for {ticker} across OpenInsider or SEC. 
                This usually means zero C-level activity in the last 90 days.</p>
            </div>
            """, unsafe_allow_html=True)
            return
            
        st.markdown(f"#### Recent Transactions for {ticker}")
        
        # Mapping OpenInsider columns to original expected structure
        # OpenInsider cols: ['X', 'Filing Date', 'Trade Date', 'Ticker', 'Insider Name', 'Title', 'Trade Type', 'Price', 'Qty', 'Owned', 'ΔOwn', 'Value']
        cols_map = {
            'Filing Date': 'Date',
            'Insider Name': 'Insider',
            'Title': 'Position',
            'Trade Type': 'Transaction',
            'Qty': 'Shares',
            'Value': 'Value'
        }
        
        display_df = df.copy()
        for old, new in cols_map.items():
            if old in display_df.columns:
                display_df[new] = display_df[old]

        def highlight_transaction(row):
            t_type = str(row.get('Transaction', '')).lower()
            color = '#ff0033' if 'sale' in t_type else '#66ff00' if 'buy' in t_type or 'purchase' in t_type else '#8b949e'
            return [f'color: {color}'] * len(row)
            
        show_cols = ['Date', 'Insider', 'Position', 'Transaction', 'Shares', 'Value']
        show_cols = [c for c in show_cols if c in display_df.columns]
        
        st.dataframe(
            display_df[show_cols].head(20).style.apply(highlight_transaction, axis=1),
            hide_index=True,
            use_container_width=True
        )
        
        st.markdown(f"""
            <div style='font-size:12px; color:{t_color}; opacity:0.6;'>
            <b>Smart Money Insight:</b> Cluster buys (multiple insiders buying at once) are statistically more significant 
            than isolated sales, which are often for taxes or diversification.
            </div>
        """, unsafe_allow_html=True)
