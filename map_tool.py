import streamlit as st
import pandas as pd

def run_map_tool():
    st.title("🌐 Map Explorer")

    # 1. Initialize Session State if empty
    if "map_points" not in st.session_state or st.session_state.map_points is None:
        # Default to a central location (e.g., London or NYC)
        st.session_state.map_points = pd.DataFrame({
            'lat': [40.7128],
            'lon': [-74.0060],
            'name': ['New York City']
        })

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📍 Drop a Pin")
        # Use a form to prevent the app from refreshing on every single keystroke
        with st.form("map_form"):
            name = st.text_input("Place Name", value="My Location")
            lat = st.number_input("Latitude", value=0.0, format="%.6f")
            lon = st.number_input("Longitude", value=0.0, format="%.6f")
            submitted = st.form_submit_button("Add to Map")
            
            if submitted:
                new_row = pd.DataFrame({'lat': [lat], 'lon': [lon], 'name': [name]})
                st.session_state.map_points = pd.concat([st.session_state.map_points, new_row], ignore_index=True)
                st.rerun()

        if st.button("🗑️ Clear Map"):
            st.session_state.map_points = pd.DataFrame(columns=['lat', 'lon', 'name'])
            st.rerun()

    with col2:
        # 2. The Condition: Only show if there is data
        if not st.session_state.map_points.empty:
            # Streamlit map MUST have columns named 'lat' and 'lon' (lowercase)
            st.map(st.session_state.map_points, color="#FF4B4B")
            st.dataframe(st.session_state.map_points, use_container_width=True)
        else:
            st.info("The map is currently empty. Enter coordinates on the left to see them here!")