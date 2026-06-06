import streamlit as st
import pickle
import numpy as np
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# ── Load Model and Encoders ───────────────────────────────
model       = pickle.load(open("model.pkl",       "rb"))
le_day      = pickle.load(open("le_day.pkl",      "rb"))
le_weather  = pickle.load(open("le_weather.pkl",  "rb"))
le_location = pickle.load(open("le_location.pkl", "rb"))

# ── Weather API ───────────────────────────────────────────
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response     = requests.get(url)
        data         = response.json()
        condition    = data["weather"][0]["main"]
        current_hour = datetime.now().hour
        if condition in ["Rain", "Drizzle", "Thunderstorm"]:
            return "Rainy", "🌧️"
        elif condition == "Clouds":
            return "Cloudy", "☁️"
        elif condition == "Clear":
            if 20 <= current_hour or current_hour < 6:
                return "Cloudy", "🌙"
            else:
                return "Sunny", "☀️"
        else:
            return "Windy", "💨"
    except:
        return "Cloudy", "☁️"

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title = "Surge Pricing Engine",
    page_icon  = "⚡",
    layout     = "centered"
)

st.markdown("""
<style>
/* Hide top toolbar */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Hide bottom manage app bar */
footer {
    display: none !important;
}

/* Hide the deploy button */
.stDeployButton {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State Defaults ────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "base_price" not in st.session_state:
    st.session_state.base_price = 30

# ── Theme Toggle ──────────────────────────────────────────
col_toggle1, col_toggle2, col_toggle3 = st.columns([6, 1, 1])
with col_toggle3:
    if st.session_state.dark_mode:
        if st.button("☀️", help="Switch to Light Mode"):
            st.session_state.dark_mode = False
            st.rerun()
    else:
        if st.button("🌙", help="Switch to Dark Mode"):
            st.session_state.dark_mode = True
            st.rerun()

dark = st.session_state.dark_mode

# ── Theme Variables ───────────────────────────────────────
if dark:
    app_bg         = "#020408"
    card_bg        = "rgba(255,255,255,0.02)"
    card_border    = "rgba(0, 255, 163, 0.2)"
    card_top_line  = "rgba(0,255,163,0.5)"
    item_bg        = "rgba(0,0,0,0.4)"
    item_border    = "rgba(0,255,163,0.15)"
    title_gradient = "linear-gradient(90deg, #00ffa3, #00c8ff, #b400ff)"
    subtitle_color = "rgba(0, 200, 255, 0.6)"
    label_color    = "rgba(0, 200, 255, 0.7)"
    value_color    = "#00ffa3"
    key_color      = "rgba(255,255,255,0.3)"
    price_color    = "#ffffff"
    arrow_color    = "rgba(0,200,255,0.5)"
    footer_color   = "rgba(255,255,255,0.3)"
    bar_bg         = "rgba(255,255,255,0.05)"
    glow_from      = "rgba(0,255,163,0.3)"
    glow_to        = "rgba(0,200,255,0.5)"
    radial1        = "rgba(0, 255, 163, 0.04)"
    radial2        = "rgba(0, 200, 255, 0.04)"
    radial3        = "rgba(180, 0, 255, 0.04)"
    input_bg       = "rgba(0,0,0,0.5)"
    input_border   = "rgba(0,255,163,0.3)"
    input_color    = "#00ffa3"
    radio_color    = "rgba(255,255,255,0.7)"
    mult_gradient  = "linear-gradient(90deg, #00ffa3, #00c8ff)"
    multiplier_sub = "rgba(255,255,255,0.3)"
else:
    app_bg         = "#f0f4f8"
    card_bg        = "rgba(255,255,255,0.9)"
    card_border    = "rgba(0, 150, 100, 0.3)"
    card_top_line  = "rgba(0,150,100,0.6)"
    item_bg        = "rgba(240,250,245,0.8)"
    item_border    = "rgba(0,150,100,0.2)"
    title_gradient = "linear-gradient(90deg, #00875a, #0077aa, #6600cc)"
    subtitle_color = "rgba(0, 100, 160, 0.8)"
    label_color    = "rgba(0, 100, 160, 0.9)"
    value_color    = "#00875a"
    key_color      = "rgba(0,0,0,0.4)"
    price_color    = "#111111"
    arrow_color    = "rgba(0,100,180,0.6)"
    footer_color   = "rgba(0,0,0,0.35)"
    bar_bg         = "rgba(0,0,0,0.08)"
    glow_from      = "rgba(0,180,120,0.2)"
    glow_to        = "rgba(0,150,200,0.3)"
    radial1        = "rgba(0, 200, 130, 0.06)"
    radial2        = "rgba(0, 150, 220, 0.06)"
    radial3        = "rgba(120, 0, 200, 0.04)"
    input_bg       = "rgba(255,255,255,0.9)"
    input_border   = "rgba(0,150,100,0.4)"
    input_color    = "#00875a"
    radio_color    = "rgba(0,0,0,0.7)"
    mult_gradient  = "linear-gradient(90deg, #00875a, #0077aa)"
    multiplier_sub = "rgba(0,0,0,0.35)"

# ── Custom CSS ────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

* {{ box-sizing: border-box; }}

.stApp {{
    background: {app_bg} !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, {radial1} 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, {radial2} 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, {radial3} 0%, transparent 50%) !important;
}}

.main-title {{
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    background: {title_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 0.2rem;
    animation: glow 3s ease-in-out infinite alternate;
}}

@keyframes glow {{
    from {{ filter: drop-shadow(0 0 8px {glow_from}); }}
    to   {{ filter: drop-shadow(0 0 20px {glow_to}); }}
}}

.sub-title {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.95rem;
    color: {subtitle_color};
    text-align: center;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}}

.neon-card {{
    background: {card_bg};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}}

.neon-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, {card_top_line}, transparent);
}}

.card-label {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {label_color};
    margin-bottom: 0.8rem;
}}

.condition-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 1rem 0;
}}

.condition-item {{
    background: {item_bg};
    border: 1px solid {item_border};
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
}}

.condition-emoji {{
    font-size: 1.8rem;
    display: block;
    margin-bottom: 0.3rem;
}}

.condition-value {{
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: {value_color};
    display: block;
}}

.condition-key {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: {key_color};
    display: block;
    margin-top: 0.2rem;
}}

.price-display {{
    text-align: center;
    padding: 2rem 0;
}}

.multiplier-value {{
    font-family: 'Orbitron', monospace;
    font-size: 4rem;
    font-weight: 900;
    background: {mult_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    animation: pulse 2s ease-in-out infinite;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50%       {{ opacity: 0.8; }}
}}

.price-row {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    margin-top: 1.5rem;
}}

.price-box {{ text-align: center; }}

.price-label {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {multiplier_sub};
}}

.price-amount {{
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: {price_color};
}}

.price-amount-final {{
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: {value_color};
}}

.price-arrow {{
    font-size: 1.5rem;
    color: {arrow_color};
}}

.demand-bar-bg {{
    background: {bar_bg};
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}}

.demand-bar-fill {{
    height: 100%;
    border-radius: 999px;
}}

.status-badge {{
    display: inline-block;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-weight: 600;
    margin-top: 0.8rem;
}}

.demand-score-text {{
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    color: {footer_color};
    text-align: center;
    margin-top: 1rem;
    letter-spacing: 2px;
    padding-bottom: 2rem;
}}

label {{
    color: {label_color} !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 1px !important;
}}

.stSelectbox > div > div {{
    background: {input_bg} !important;
    border: 1px solid {input_border} !important;
    border-radius: 10px !important;
    color: {input_color} !important;
    font-family: 'Rajdhani', sans-serif !important;
}}

.stRadio label {{
    color: {radio_color} !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown('<div class="main-title">⚡ SURGE ENGINE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hyper-Local Dynamic Pricing System</div>', unsafe_allow_html=True)

# ── Auto Fetch Time and Date ──────────────────────────────
from datetime import timezone, timedelta
IST = timezone(timedelta(hours=5, minutes=30))
now = datetime.now(IST)
hour     = now.hour
day_name = now.strftime("%A")
date_str = now.strftime("%d %b %Y")
time_str = now.strftime("%I:%M %p")
day_type = "Weekend" if day_name in ["Saturday", "Sunday"] else "Weekday"

# ── Location ──────────────────────────────────────────────
st.markdown(f'<div class="neon-card"><div class="card-label">📍 Delivery Zone</div>', unsafe_allow_html=True)
location = st.selectbox(
    "Select area",
    ["Hitech City", "Banjara Hills", "Madhapur", "Kukatpally", "Dilsukhnagar"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ── API + Weather ─────────────────────────────────────────
API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
city_map = {
    "Hitech City"   : "Hyderabad",
    "Banjara Hills" : "Hyderabad",
    "Madhapur"      : "Hyderabad",
    "Kukatpally"    : "Hyderabad",
    "Dilsukhnagar"  : "Hyderabad"
}
weather, weather_emoji = get_weather(city_map[location], API_KEY)

# ── Event Input ───────────────────────────────────────────
st.markdown(f'<div class="neon-card"><div class="card-label">🎯 Local Event Status</div>', unsafe_allow_html=True)
event_choice = st.radio(
    "Event",
    ["No active event", "Event happening today"],
    label_visibility="collapsed",
    horizontal=True
)
event = 1 if "Event" in event_choice else 0
st.markdown('</div>', unsafe_allow_html=True)

# ── Base Price Input ──────────────────────────────────────
st.markdown(f'<div class="neon-card"><div class="card-label">💵 Base Delivery Fee</div>', unsafe_allow_html=True)
base_price = st.number_input(
    "₹ Enter base delivery fee",
    min_value = 10,
    max_value = 500,
    value     = st.session_state.base_price,  # ← uses session state
    step      = 5,
)
st.session_state.base_price = base_price  # ← saves to session state
st.markdown('</div>', unsafe_allow_html=True)

# ── Live Conditions ───────────────────────────────────────
st.markdown(f"""
<div class="neon-card">
    <div class="card-label">⚡ Live Conditions — {date_str}</div>
    <div class="condition-grid">
        <div class="condition-item">
            <span class="condition-emoji">🕐</span>
            <span class="condition-value">{time_str}</span>
            <span class="condition-key">Time</span>
        </div>
        <div class="condition-item">
            <span class="condition-emoji">📅</span>
            <span class="condition-value">{day_name[:3].upper()}</span>
            <span class="condition-key">{day_type}</span>
        </div>
        <div class="condition-item">
            <span class="condition-emoji">{weather_emoji}</span>
            <span class="condition-value">{weather.upper()}</span>
            <span class="condition-key">Weather</span>
        </div>
        <div class="condition-item">
            <span class="condition-emoji">{"🎉" if event else "😴"}</span>
            <span class="condition-value">{"ON" if event else "OFF"}</span>
            <span class="condition-key">Event</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Calculate Demand ──────────────────────────────────────
demand = 0
if 12 <= hour <= 14:      demand += 3
elif 19 <= hour <= 21:    demand += 3
elif 8 <= hour <= 10:     demand += 2
if weather == "Rainy":    demand += 3
elif weather == "Cloudy": demand += 1
if day_type == "Weekend": demand += 2
else:                     demand += 1
if event == 1:            demand += 3
if location in ["Hitech City", "Banjara Hills"]: demand += 2
elif location == "Madhapur":                     demand += 1
demand = max(0, demand)

# ── Encode + Predict ──────────────────────────────────────
day_enc = le_day.transform([day_type])[0]
wea_enc = le_weather.transform([weather])[0]
loc_enc = le_location.transform([location])[0]

input_data       = np.array([[hour, day_enc, wea_enc, loc_enc, event, demand]])
price_multiplier = round(model.predict(input_data)[0], 2)
final_price      = round(st.session_state.base_price * price_multiplier, 2)

# ── Colors based on multiplier ────────────────────────────
max_demand = 13
demand_pct = min(int((demand / max_demand) * 100), 100)

if dark:
    if price_multiplier >= 1.8:
        bar_color    = "linear-gradient(90deg, #ff6b00, #ff0055)"
        status_txt   = "🔴 CRITICAL SURGE"
        badge_bg     = "rgba(255,0,85,0.15)"
        badge_color  = "#ff0055"
        badge_border = "rgba(255,0,85,0.4)"
    elif price_multiplier >= 1.4:
        bar_color    = "linear-gradient(90deg, #ffaa00, #ff6b00)"
        status_txt   = "🟡 HIGH DEMAND"
        badge_bg     = "rgba(255,170,0,0.15)"
        badge_color  = "#ffaa00"
        badge_border = "rgba(255,170,0,0.4)"
    elif price_multiplier >= 1.1:
        bar_color    = "linear-gradient(90deg, #00c8ff, #00ffa3)"
        status_txt   = "🔵 MODERATE SURGE"
        badge_bg     = "rgba(0,200,255,0.15)"
        badge_color  = "#00c8ff"
        badge_border = "rgba(0,200,255,0.4)"
    else:
        bar_color    = "linear-gradient(90deg, #00ffa3, #00c8ff)"
        status_txt   = "🟢 NORMAL PRICING"
        badge_bg     = "rgba(0,255,163,0.15)"
        badge_color  = "#00ffa3"
        badge_border = "rgba(0,255,163,0.4)"
else:
    if price_multiplier >= 1.8:
        bar_color    = "linear-gradient(90deg, #cc4400, #cc0033)"
        status_txt   = "🔴 CRITICAL SURGE"
        badge_bg     = "rgba(200,0,50,0.1)"
        badge_color  = "#cc0033"
        badge_border = "rgba(200,0,50,0.3)"
    elif price_multiplier >= 1.4:
        bar_color    = "linear-gradient(90deg, #cc8800, #cc4400)"
        status_txt   = "🟡 HIGH DEMAND"
        badge_bg     = "rgba(200,130,0,0.1)"
        badge_color  = "#996600"
        badge_border = "rgba(200,130,0,0.3)"
    elif price_multiplier >= 1.1:
        bar_color    = "linear-gradient(90deg, #0077aa, #00875a)"
        status_txt   = "🔵 MODERATE SURGE"
        badge_bg     = "rgba(0,100,170,0.1)"
        badge_color  = "#0077aa"
        badge_border = "rgba(0,100,170,0.3)"
    else:
        bar_color    = "linear-gradient(90deg, #00875a, #0077aa)"
        status_txt   = "🟢 NORMAL PRICING"
        badge_bg     = "rgba(0,135,90,0.1)"
        badge_color  = "#00875a"
        badge_border = "rgba(0,135,90,0.3)"

# ── Price Card ────────────────────────────────────────────
st.markdown(f"""
<div class="neon-card">
    <div class="card-label">💰 Surge Calculation</div>
    <div class="price-display">
        <div style="font-family:'Rajdhani',sans-serif; font-size:0.7rem; letter-spacing:3px; color:{multiplier_sub}; text-transform:uppercase; margin-bottom:0.5rem;">Price Multiplier</div>
        <div class="multiplier-value">{price_multiplier}x</div>
        <div class="price-row">
            <div class="price-box">
                <div class="price-label">Base</div>
                <div class="price-amount">₹{st.session_state.base_price}</div>
            </div>
            <div class="price-arrow">→</div>
            <div class="price-box">
                <div class="price-label">Final Price</div>
                <div class="price-amount-final">₹{final_price}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Demand Card ───────────────────────────────────────────
st.markdown(f"""
<div class="neon-card">
    <div class="card-label">📊 Demand Analysis</div>
    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <span style="font-family:'Rajdhani',sans-serif; font-size:0.7rem; letter-spacing:2px; color:{key_color}; text-transform:uppercase;">Demand Level</span>
        <span style="font-family:'Orbitron',monospace; font-size:0.7rem; color:{badge_color};">{demand_pct}%</span>
    </div>
    <div class="demand-bar-bg">
        <div class="demand-bar-fill" style="width:{demand_pct}%; background:{bar_color};"></div>
    </div>
    <div style="text-align:center; margin-top:1.2rem;">
        <span class="status-badge" style="background:{badge_bg}; color:{badge_color}; border:1px solid {badge_border};">
            {status_txt}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown(f"""
<div class="demand-score-text">
    DEMAND SCORE: {demand} / {max_demand} &nbsp;|&nbsp; ZONE: {location.upper()} &nbsp;|&nbsp; {date_str}
</div>
""", unsafe_allow_html=True)