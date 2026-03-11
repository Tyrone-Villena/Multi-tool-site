import streamlit as st
import math

def run_calculator_tool():
    # --- 1. STATE INITIALIZATION ---
    if "calc_expression" not in st.session_state:
        st.session_state.calc_expression = ""
    if "calc_history" not in st.session_state:
        st.session_state.calc_history = []
    if "calc_theme" not in st.session_state:
        st.session_state.calc_theme = "#00FF00" # Classic Matrix Green

    st.title("🚀 Super-Scientific Station")

    # --- 2. LAYOUT: MAIN & SIDEBAR ---
    main_col, hist_col = st.columns([3, 1])

    with main_col:
        # Theme Picker (Mini)
        t1, t2, t3 = st.columns([2, 1, 1])
        with t3:
            st.session_state.calc_theme = st.color_picker("Display Color", st.session_state.calc_theme, label_visibility="collapsed")

        # Digital Screen
        st.markdown(f"""
            <div style="background-color: #0E1117; padding: 25px; border-radius: 15px; border: 3px solid #31333F; margin-bottom: 20px; box-shadow: inset 0 0 10px #000;">
                <p style="color: #666; font-family: monospace; margin: 0; text-align: left; font-size: 12px;">SCIENTIFIC MODE ACTIVE</p>
                <h1 style="color: {st.session_state.calc_theme}; font-family: 'Courier New', monospace; text-align: right; margin: 0; text-shadow: 0 0 10px {st.session_state.calc_theme}55;">
                    {st.session_state.calc_expression if st.session_state.calc_expression else "0"}
                </h1>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🔢 Standard", "🧪 Scientific", "⚖️ Unit Converter"])

        # --- LOGIC HELPERS ---
        def evaluate():
            try:
                raw_expr = st.session_state.calc_expression
                expr = raw_expr.replace('^', '**').replace('÷', '/').replace('×', '*')
                # Math Context
                context = {
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "sqrt": math.sqrt, "pi": math.pi, "e": math.e, "log": math.log10
                }
                result = eval(expr, {"__builtins__": None}, context)
                formatted_res = str(round(result, 6))
                
                # Update History
                st.session_state.calc_history.insert(0, f"{raw_expr} = {formatted_res}")
                st.session_state.calc_expression = formatted_res
            except:
                st.error("Syntax Error")
                st.session_state.calc_expression = ""

        # --- TAB 1: STANDARD ---
        with tab1:
            rows = [
                ['C', '(', ')', '÷'],
                ['7', '8', '9', '×'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['0', '.', '=', '⌫']
            ]
            for row in rows:
                cols = st.columns(4)
                for i, btn in enumerate(row):
                    if cols[i].button(btn, key=f"std_{btn}", use_container_width=True):
                        if btn == "=": evaluate()
                        elif btn == "C": st.session_state.calc_expression = ""
                        elif btn == "⌫": st.session_state.calc_expression = st.session_state.calc_expression[:-1]
                        elif btn == "×": st.session_state.calc_expression += "*"
                        elif btn == "÷": st.session_state.calc_expression += "/"
                        else: st.session_state.calc_expression += btn
                        st.rerun()

        # --- TAB 2: SCIENTIFIC ---
        with tab2:
            sc_rows = [
                ['sin', 'cos', 'tan', 'sqrt'],
                ['log', 'pi', 'e', '^']
            ]
            for row in sc_rows:
                cols = st.columns(4)
                for i, btn in enumerate(row):
                    if cols[i].button(btn, key=f"sci_{btn}", use_container_width=True):
                        if btn in ['sin', 'cos', 'tan', 'log', 'sqrt']:
                            st.session_state.calc_expression += f"{btn}("
                        else:
                            st.session_state.calc_expression += btn
                        st.rerun()
            st.info("Trigonometry uses Radians. Tip: use `pi` for 180°.")

        # --- TAB 3: UNIT CONVERTER ---
        with tab3:
            c_type = st.selectbox("Category", ["Length (m to ft)", "Temp (C to F)", "Weight (kg to lbs)"])
            val = st.number_input("Value to convert:", value=1.0)
            
            if c_type == "Length (m to ft)":
                res = val * 3.28084
                st.metric("Result", f"{res:.2f} ft")
            elif c_type == "Temp (C to F)":
                res = (val * 9/5) + 32
                st.metric("Result", f"{res:.2f} °F")
            elif c_type == "Weight (kg to lbs)":
                res = val * 2.20462
                st.metric("Result", f"{res:.2f} lbs")

    # --- 3. SIDEBAR: HISTORY ---
    with hist_col:
        st.subheader("📜 History")
        if st.button("Clear Log", use_container_width=True):
            st.session_state.calc_history = []
            st.rerun()
        
        for item in st.session_state.calc_history[:10]:
            st.text(item)
            st.divider()