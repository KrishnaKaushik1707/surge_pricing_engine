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
        response  = requests.get(url)
        data      = response.json()
        condition = data["weather"][0]["main"]
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

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #020408 !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(0, 255, 163, 0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 200, 255, 0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, rgba(180, 0, 255, 0.04) 0%, transparent 50%) !important;
}

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00ffa3, #00c8ff, #b400ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 0.2rem;
    animation: glow 3s ease-in-out infinite alternate;
}

@keyframes glow {
    from { filter: drop-shadow(0 0 8px rgba(0,255,163,0.3)); }
    to   { filter: drop-shadow(0 0 20px rgba(0,200,255,0.5)); }
}

.sub-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.95rem;
    color: rgba(0, 200, 255, 0.6);
    text-align: center;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.neon-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(0, 255, 163, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}

.neon-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,163,0.5), transparent);
}

.card-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(0, 200, 255, 0.7);
    margin-bottom: 0.8rem;
}

.condition-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 1rem 0;
}

.condition-item {
    background: rgba(0,0,0,0.4);
    border: 1px solid rgba(0,255,163,0.15);
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
}

.condition-emoji {
    font-size: 1.8rem;
    display: block;
    margin-bottom: 0.3rem;
}

.condition-value {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: #00ffa3;
    display: block;
}

.condition-key {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
    display: block;
    margin-top: 0.2rem;
}

.price-display {
    text-align: center;
    padding: 2rem 0;
}

.multiplier-value {
    font-family: 'Orbitron', monospace;
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00ffa3, #00c8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.8; }
}

.price-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    margin-top: 1.5rem;
}

.price-box { text-align: center; }

.price-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
}

.price-amount {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
}

.price-amount.final {
    color: #00ffa3;
    font-size: 1.8rem;
}

.price-arrow {
    font-size: 1.5rem;
    color: rgba(0,200,255,0.5);
}

.demand-bar-bg {
    background: rgba(255,255,255,0.05);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}

.demand-bar-fill {
    height: 100%;
    border-radius: 999px;
}

.status-badge {
    display: inline-block;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-weight: 600;
    margin-top: 0.8rem;
}

.demand-score-text {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.3);
    text-align: center;
    margin-top: 1rem;
    letter-spacing: 2px;
}

label {
    color: rgba(0,200,255,0.8) !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 1px !important;
}

.stSelectbox > div > div {
    background: rgba(0,0,0,0.5) !important;
    border: 1px solid rgba(0,255,163,0.3) !important;
    border-radius: 10px !important;
    color: #00ffa3 !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.stRadio label {
    color: rgba(255,255,255,0.7) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown('<div class="main-title">⚡ SURGE ENGINE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hyper-Local Dynamic Pricing System</div>', unsafe_allow_html=True)

# ── Auto Fetch Time and Date ──────────────────────────────
now      = datetime.now()
hour     = now.hour
day_name = now.strftime("%A")
date_str = now.strftime("%d %b %Y")
time_str = now.strftime("%I:%M %p")
day_type = "Weekend" if day_name in ["Saturday", "Sunday"] else "Weekday"

# ── Location ──────────────────────────────────────────────
st.markdown('<div class="neon-card"><div class="card-label">📍 Delivery Zone</div>', unsafe_allow_html=True)
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
st.markdown('<div class="neon-card"><div class="card-label">🎯 Local Event Status</div>', unsafe_allow_html=True)
event_choice = st.radio(
    "Event",
    ["No active event", "Event happening today"],
    label_visibility="collapsed",
    horizontal=True
)
event = 1 if "Event" in event_choice else 0
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
base_price       = 30
final_price      = round(base_price * price_multiplier, 2)

# ── Colors based on multiplier ────────────────────────────
max_demand = 13
demand_pct = min(int((demand / max_demand) * 100), 100)

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

# ── Price Card ────────────────────────────────────────────
st.markdown(f"""
<div class="neon-card">
    <div class="card-label">💰 Surge Calculation</div>
    <div class="price-display">
        <div style="font-family:'Rajdhani',sans-serif; font-size:0.7rem; letter-spacing:3px; color:rgba(255,255,255,0.3); text-transform:uppercase; margin-bottom:0.5rem;">Price Multiplier</div>
        <div class="multiplier-value">{price_multiplier}x</div>
        <div class="price-row">
            <div class="price-box">
                <div class="price-label">Base</div>
                <div class="price-amount">₹{base_price}</div>
            </div>
            <div class="price-arrow">→</div>
            <div class="price-box">
                <div class="price-label">Final Price</div>
                <div class="price-amount final">₹{final_price}</div>
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
        <span style="font-family:'Rajdhani',sans-serif; font-size:0.7rem; letter-spacing:2px; color:rgba(255,255,255,0.3); text-transform:uppercase;">Demand Level</span>
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