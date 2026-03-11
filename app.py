import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from weather_tool import run_weather_tool
from clock_tool import run_clock_tool
from memo_tool import run_memo_tool
from links_tool import run_links_tool
from calculator_tool import run_calculator_tool
from map_tool import run_map_tool

# --- 1. MUST BE FIRST ---
st.set_page_config(page_title="Multi-Tool OS", layout="wide", page_icon="🛠️")

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    # A. Mini Digital Clock
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: #262730; border-radius: 10px; border: 1px solid #444;">
            <h2 style="margin: 0; color: #00FF00; font-family: monospace;">{current_time}</h2>
            <p style="margin: 0; color: #888; font-size: 12px;">{datetime.now().strftime("%A, %b %d")}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("🛠️ Tool Selection")
    tool = st.radio(
        "Go to:", 
        ["Chart Creator", "Weather Forecast", "World Clock", "Quick Memo", "Quick Links", "Calculator", "Map Explorer"],
    )
    
    st.divider()

    # B. Global Quick Tasks (Indented correctly to stay in sidebar)
    st.subheader("✅ Global Tasks")
    if "todo_list" not in st.session_state:
        st.session_state.todo_list = []
    
    new_task = st.text_input("Quick add task:", key="sidebar_todo", label_visibility="collapsed", placeholder="New task...")
    if st.button("➕ Add", use_container_width=True):
        if new_task:
            st.session_state.todo_list.append({"task": new_task, "done": False})
            st.rerun()
            
    # Task display loop inside the sidebar block
    for i, item in enumerate(st.session_state.todo_list):
        cols = st.columns([0.8, 0.2])
        is_done = cols[0].checkbox(item["task"], value=item["done"], key=f"side_t_{i}")
        st.session_state.todo_list[i]["done"] = is_done
        if cols[1].button("🗑️", key=f"side_d_{i}"):
            st.session_state.todo_list.pop(i)
            st.rerun()

# --- 3. TOOL ROUTING ---
if tool == "Chart Creator":
    st.title("📊 Advanced Chart Studio")
    
    st.subheader("1. Prepare Your Data")
    upload_file = st.file_uploader("Upload a CSV (Optional)", type=["csv"])
    
    if upload_file is not None:
        base_df = pd.read_csv(upload_file)
    else:
        base_df = pd.DataFrame({
            "Category": ["A", "B", "C", "D", "E"],
            "Values": [25, 40, 15, 30, 20]
        })

    st.info("💡 Edit cells below or add rows by clicking the '+' at the bottom of the table.")
    df = st.data_editor(base_df, num_rows="dynamic", use_container_width=True)

    st.divider()

    st.subheader("2. Quick Insights")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        stat_col = st.selectbox("Select column for statistics:", numeric_cols)
        m1, m2, m3 = st.columns(3)
        m1.metric("Average", f"{df[stat_col].mean():.2f}")
        m2.metric("Maximum", f"{df[stat_col].max()}")
        m3.metric("Minimum", f"{df[stat_col].min()}")
    else:
        st.warning("Add some numbers to the table to see statistics!")

    st.divider()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Chart Settings")
        all_cols = df.columns.tolist()
        x_axis = st.selectbox("Select X-Axis", all_cols, index=0)
        y_axis = st.selectbox("Select Y-Axis", all_cols, index=1 if len(all_cols) > 1 else 0)
        chart_type = st.selectbox("Type", ["Bar", "Line", "Scatter", "Area", "Pie", "Histogram", "Box Plot"])
        chart_color = st.color_picker("Color", "#FF4B4B")

    with col2:
        st.subheader("Live Preview")
        try:
            if chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=[chart_color])
            elif chart_type == "Line":
                fig = px.line(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=[chart_color])
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=y_axis, template="plotly_dark", color_discrete_sequence=[chart_color])
            elif chart_type == "Pie":
                fig = px.pie(df, names=x_axis, values=y_axis, template="plotly_dark")
            elif chart_type == "Area":
                fig = px.area(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=[chart_color])
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=[chart_color])
            elif chart_type == "Box Plot":
                fig = px.box(df, y=y_axis, template="plotly_dark", color_discrete_sequence=[chart_color])
                
            st.plotly_chart(fig, use_container_width=True)

            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download CSV", data=csv_data, file_name="data.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Error: {e}")

elif tool == "Weather Forecast":
    run_weather_tool()

elif tool == "World Clock":
    run_clock_tool()

elif tool == "Quick Memo":
    run_memo_tool()

elif tool == "Quick Links":
    run_links_tool()

elif tool == "Calculator":
    run_calculator_tool()

elif tool == "Map Explorer":
    from map_tool import run_map_tool # Make sure the import is correct
    run_map_tool()