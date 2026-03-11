import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

def get_weather_symbol(code):
    """Translates WMO Weather Interpretation Codes to Emojis"""
    weather_map = {
        0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
        45: "🌫️", 51: "🌦️", 61: "🌧️", 63: "🌧️", 65: "🌧️",
        80: "🌦️", 95: "⛈️", 96: "⛈️"
    }
    # Default to a thermometer if code is unknown
    return weather_map.get(code, "🌡️")

def run_weather_tool():
    st.title("🌤️ Philippines Weather Forecast")
    
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("Enter City Name", "Manila")
    with col2:
        unit = st.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"])

    # 1. Geocoding
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geo_data = requests.get(geo_url).json()

    if "results" in geo_data:
        res = geo_data["results"][0]
        lat, lon = res["latitude"], res["longitude"]
        st.write(f"📍 **Location:** {res['name']}, {res.get('country', '')}")

        # 2. Fetching Weather Data
        temp_unit = "celsius" if unit == "Celsius" else "fahrenheit"
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min"
            f"&hourly=temperature_2m&timezone=auto&temperature_unit={temp_unit}"
        )
        
        response = requests.get(weather_url).json()
        
        # --- FIX: Defining 'current' properly ---
        current = response.get("current", {})
        current_symbol = get_weather_symbol(current.get('weather_code', 0))
        
        # 3. Current Condition Display
        st.divider()
        st.subheader(f"Current Condition: {current_symbol}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Temperature", f"{current.get('temperature_2m', 'N/A')}°{unit[0]}")
        m2.metric("Humidity", f"{current.get('relative_humidity_2m', 'N/A')}%")
        m3.metric("Wind Speed", f"{current.get('wind_speed_10m', 'N/A')} km/h")
        st.divider()

        # 4. Daily Forecast Symbols (Now and Tomorrow)
        st.subheader("📅 7-Day Outlook")
        daily = response.get("daily", {})
        day_cols = st.columns(7)
        
        for i in range(7):
            with day_cols[i]:
                date_str = daily["time"][i]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                display_date = date_obj.strftime("%a, %b %d")
                
                if i == 0: display_date = "Today"
                if i == 1: display_date = "Tomorrow"
                
                day_symbol = get_weather_symbol(daily["weather_code"][i])
                st.markdown(f"**{display_date}**")
                st.markdown(f"### {day_symbol}")
                st.caption(f"H:{daily['temperature_2m_max'][i]}° L:{daily['temperature_2m_min'][i]}°")

        st.divider()

        # 5. Hourly Trend Chart
        st.subheader("📈 Hourly Temperature Trend")
        hourly_df = pd.DataFrame({
            "Time": pd.to_datetime(response["hourly"]["time"]),
            "Temp": response["hourly"]["temperature_2m"]
        })
        fig = px.line(hourly_df.head(48), x="Time", y="Temp", template="plotly_dark")
        fig.update_traces(line_color='#00d1ff', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("City not found! Please check spelling.")