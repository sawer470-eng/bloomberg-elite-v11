import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import textwrap

@st.cache_data(ttl=3600)
def get_options_sentiment_syndicate(ticker):
    """
    Syndicate fetching for Sentiment (Finviz -> MarketWatch)
    """
    data = {
        "short_float": "N/A",
        "short_ratio": "N/A",
        "inst_own": "N/A",
        "inst_trans": "N/A",
        "pc_ratio": "N/A"
    }
    
    try:
        url = f"https://finviz.com/quote.ashx?t={ticker}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        table = soup.find('table', {'class': 'snapshot-table2'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                for i, cell in enumerate(cells):
                    txt = cell.text.strip()
                    if "Short Float" in txt: data["short_float"] = cells[i+1].text.strip()
                    if "Short Ratio" in txt: data["short_ratio"] = cells[i+1].text.strip()
                    if "Inst Own" in txt: data["inst_own"] = cells[i+1].text.strip()
                    if "Inst Trans" in txt: data["inst_trans"] = cells[i+1].text.strip()
    except:
        pass
        
    return data

def render_options_data():
            with c1:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>PUT VOLUME</div><div class='metric-value'>{put_vol:,.0f}</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>CALL VOLUME</div><div class='metric-value'>{call_vol:,.0f}</div></div>", unsafe_allow_html=True)
            with c3:
                color = "#ff0033" if pc_vol_ratio > 1 else "#66ff00"
                sentiment = "BEARISH" if pc_vol_ratio > 1 else "BULLISH"
                st.markdown(f"<div class='metric-card'><div class='metric-title'>P/C VOL RATIO</div><div class='metric-value' style='color:{color}'>{pc_vol_ratio:.2f}</div><div style='color:{color}; font-size:12px;'>{sentiment}</div></div>", unsafe_allow_html=True)
            with c4:
                oi_color = "#ff0033" if pc_oi_ratio > 1.2 else "#66ff00"
                oi_sentiment = "BEARISH EXTREME" if pc_oi_ratio > 1.2 else "NORMAL/BULLISH"
                st.markdown(f"<div class='metric-card'><div class='metric-title'>P/C OI RATIO</div><div class='metric-value' style='color:{oi_color}'>{pc_oi_ratio:.2f}</div><div style='color:{oi_color}; font-size:12px;'>{oi_sentiment}</div></div>", unsafe_allow_html=True)
                
            # Chart
            fig = go.Figure()
            fig.add_trace(go.Bar(x=calls['strike'], y=calls['volume'], name='Call Volume', marker_color='#66ff00'))
            fig.add_trace(go.Bar(x=puts['strike'], y=puts['volume'], name='Put Volume', marker_color='#ff0033'))
            
            fig.update_layout(
                title="Options Volume by Strike",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#8b949e', family="monospace"),
                barmode='group',
                xaxis_title="Strike Price",
                yaxis_title="Volume",
                xaxis=dict(showgrid=True, gridcolor='rgba(69, 162, 158, 0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(69, 162, 158, 0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error fetching options: {e}")
