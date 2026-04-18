import streamlit as st
import yfinance as yf
import textwrap
from data_engine import get_ticker_tape_data
from cot_dashboard import render_cot_dashboard
from market_data import render_market_data
from macro_data import render_macro_data
from news_feed import render_news_feed
from options_data import render_options_data
from correlation_data import render_correlation_matrix
from insider_data import render_insider_data
from tpo_data import render_tpo_data
from fair_value import render_fair_value_data
from news_impact import render_news_impact_data
from smc_scanner import render_smc_scanner
from ai_intelligence import render_ai_intelligence
from watchlists import render_watchlists
from liquidity_data import render_liquidity_data

st.set_page_config(page_title="Bloomberg Elite V3", layout="wide", page_icon="🏦")

# Theme Management
if 'theme' not in st.session_state:
    st.session_state.theme = "Obsidian Black"

st.sidebar.title("BLOOMBERG ELITE V3")
st.sidebar.markdown("---")
theme_choice = st.sidebar.select_slider(
    "UI AESTHETIC",
    options=["Obsidian Black", "Titanium Gray", "Alpine White"],
    value=st.session_state.theme
)
st.session_state.theme = theme_choice

# Define Theme Palettes
themes = {
    "Obsidian Black": {
        "bg": "radial-gradient(circle at 10% 20%, rgb(18, 18, 24) 0%, rgb(0, 0, 0) 90.2%)",
        "card_bg": "rgba(25, 27, 34, 0.45)",
        "card_border": "rgba(69, 162, 158, 0.25)",
        "text": "#c5c6c7",
        "title": "#ffffff",
        "accent": "#45a29e",
        "shadow": "rgba(0, 0, 0, 0.6)",
        "ticker_bg": "rgba(11, 12, 16, 0.9)"
    },
    "Titanium Gray": {
        "bg": "linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)",
        "card_bg": "rgba(255, 255, 255, 0.05)",
        "card_border": "rgba(255, 255, 255, 0.1)",
        "text": "#e0e0e0",
        "title": "#ffffff",
        "accent": "#ff9900",
        "shadow": "rgba(0, 0, 0, 0.4)",
        "ticker_bg": "rgba(30, 30, 30, 0.95)"
    },
    "Alpine White": {
        "bg": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        "card_bg": "rgba(255, 255, 255, 0.7)",
        "card_border": "rgba(0, 0, 0, 0.05)",
        "text": "#1a1a1a",
        "title": "#000000",
        "accent": "#2980b9",
        "shadow": "rgba(0, 0, 0, 0.1)",
        "ticker_bg": "rgba(255, 255, 255, 0.9)"
    }
}

t = themes[st.session_state.theme]

# Global CSS for Premium Glassmorphism
css_style = textwrap.dedent(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Outfit:wght@500;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
    .stApp {{
        background: {t['bg']};
        font-family: 'Inter', sans-serif;
        color: {t['text']};
    }}
    
    /* Metrics and Cards */
    .metric-card {{
        background: {t['card_bg']};
        backdrop-filter: blur(12px) saturate(180%);
        -webkit-backdrop-filter: blur(12px) saturate(180%);
        border: 1px solid {t['card_border']};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 {t['shadow']};
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .metric-card:hover {{
        transform: translateY(-8px);
        border-color: {t['accent']};
        box-shadow: 0 12px 40px 0 {t['shadow']}, 0 0 20px {t['accent']}44;
    }}
    
    .metric-title {{
        color: {t['accent']};
        font-family: 'Outfit', sans-serif;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
        opacity: 0.9;
    }}
    .metric-value {{
        color: {t['title']};
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        font-weight: 800;
        text-shadow: 0 0 15px {t['accent']}66;
    }}
    
    /* TICKER TAPE CSS */
    .ticker-wrap {{
        width: 100%;
        overflow: hidden;
        background: {t['ticker_bg']};
        backdrop-filter: blur(15px);
        box-sizing: content-box;
        border-bottom: 2px solid {t['accent']};
        white-space: nowrap;
        padding: 12px 0;
        margin-bottom: 30px;
        position: sticky;
        top: 0;
        z-index: 999;
        box-shadow: 0 4px 20px {t['shadow']};
    }}
    .ticker {{
        display: inline-block;
        padding-left: 100%;
        animation: ticker 50s linear infinite;
        font-weight: 600;
        font-size: 14px;
        font-family: 'JetBrains Mono', monospace;
        color: {t['text']};
    }}
    @keyframes ticker {{
        0%   {{ transform: translate3d(0, 0, 0); }}
        100% {{ transform: translate3d(-100%, 0, 0); }}
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {t['ticker_bg']} !important;
        border-right: 1px solid {t['card_border']};
    }}
    
    /* Headers */
    h1, h2, h3 {{
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        color: {t['title']} !important;
        background: none !important;
        -webkit-text-fill-color: {t['title']} !important;
        letter-spacing: -0.5px;
    }}
    
    /* Dataframe background fix for light mode */
    [data-testid="stExpander"] {{
        background: {t['card_bg']} !important;
    }}
</style>
""")

st.markdown(css_style, unsafe_allow_html=True)

# Inject Ticker Tape
ticker_content = get_ticker_tape_data()
tape_html = textwrap.dedent(f"""
<div class="ticker-wrap">
    <div class="ticker">
        {ticker_content} &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; {ticker_content} &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; {ticker_content}
    </div>
</div>
""")
st.markdown(tape_html, unsafe_allow_html=True)

st.sidebar.markdown("---")

# Page Routing
menu = [
    "1. SMC & COT Analysis",
    "2. Market Heatmap & Treemap",
    "3. Macro Data & Calendar",
    "4. Correlation Matrix (ELITE)",
    "5. Options Sentiment (PRO)",
    "6. Insider Tracker (ELITE)",
    "7. Volume Profile TPO (ELITE)",
    "8. Fair Value & DCF (ELITE)",
    "9. SMC Scanner (ELITE NEW)",
    "10. Liquidity & Footprint (ELITE NEW)",
    "11. AI Intelligence Lab (PRO)",
    "12. News Impact Lab (ELITE)",
    "13. Live News Feed",
    "14. Custom Watchlists (PRO)"
]

# State Management for Navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = menu[0]

choice = st.sidebar.radio("NAVIGATION", menu, index=menu.index(st.session_state.current_page))
st.session_state.current_page = choice # Update state

if choice == "1. SMC & COT Analysis":
    render_cot_dashboard()
elif choice == "2. Market Heatmap & Treemap":
    render_market_data()
elif choice == "3. Macro Data & Calendar":
    render_macro_data()
elif choice == "4. Correlation Matrix (ELITE)":
    render_correlation_matrix()
elif choice == "5. Options Sentiment (PRO)":
    render_options_data()
elif choice == "6. Insider Tracker (ELITE)":
    render_insider_data()
elif choice == "7. Volume Profile TPO (ELITE)":
    render_tpo_data()
elif choice == "8. Fair Value & DCF (ELITE)":
    render_fair_value_data()
elif choice == "9. SMC Scanner (ELITE NEW)":
    render_smc_scanner()
elif choice == "10. Liquidity & Footprint (ELITE NEW)":
    render_liquidity_data()
elif choice == "11. AI Intelligence Lab (PRO)":
    render_ai_intelligence()
elif choice == "12. News Impact Lab (ELITE)":
    render_news_impact_data()
elif choice == "13. Live News Feed":
    render_news_feed()
elif choice == "14. Custom Watchlists (PRO)":
    render_watchlists()
