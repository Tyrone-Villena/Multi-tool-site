import streamlit as st
from datetime import datetime
import pytz
import time
import pandas as pd


        
def run_clock_tool():
    st.title("⏲️ Time Management Suite")

    tab1, tab2, tab3, tab4 = st.tabs(["World Clock", "Stopwatch", "Pomodoro", "Timer"])

    # --- TAB 1: WORLD CLOCK ---
    with tab1:
        st.subheader("Current World Time")
        zones = {"Manila 🇵🇭": "Asia/Manila", "London 🇬🇧": "Europe/London", 
                 "New York 🇺🇸": "America/New_York", "Tokyo 🇯🇵": "Asia/Tokyo"}
        cols = st.columns(len(zones))
        for i, (name, zone) in enumerate(zones.items()):
            with cols[i]:
                now = datetime.now(pytz.timezone(zone))
                st.metric(name, now.strftime("%I:%M %p"))
                st.caption(now.strftime("%a, %b %d"))

    # --- TAB 2: STOPWATCH WITH LAPS ---
    with tab2:
        st.subheader("⏱️ Precise Stopwatch")
        if "sw_running" not in st.session_state: st.session_state.sw_running = False
        if "sw_start" not in st.session_state: st.session_state.sw_start = 0
        if "sw_acc" not in st.session_state: st.session_state.sw_acc = 0
        if "sw_laps" not in st.session_state: st.session_state.sw_laps = []

        def fmt(d): return f"{int(d//60):02d}:{int(d%60):02d}:{int((d%1)*100):02d}"

        c1, c2, c3 = st.columns(3)
        if not st.session_state.sw_running:
            if c1.button("▶️ Start", use_container_width=True):
                st.session_state.sw_start = time.time()
                st.session_state.sw_running = True
                st.rerun()
        else:
            if c1.button("⏸️ Pause", use_container_width=True):
                st.session_state.sw_acc += time.time() - st.session_state.sw_start
                st.session_state.sw_running = False
                st.rerun()

        if c2.button("🚩 Lap", disabled=not st.session_state.sw_running, use_container_width=True):
            total = st.session_state.sw_acc + (time.time() - st.session_state.sw_start)
            st.session_state.sw_laps.insert(0, fmt(total))
        if c3.button("🔄 Reset", use_container_width=True):
            st.session_state.update({"sw_running": False, "sw_acc": 0, "sw_laps": []})
            st.rerun()

        placeholder = st.empty()
        while st.session_state.sw_running:
            live = st.session_state.sw_acc + (time.time() - st.session_state.sw_start)
            placeholder.header(fmt(live))
            time.sleep(0.05)
        if not st.session_state.sw_running: placeholder.header(fmt(st.session_state.sw_acc))
        if st.session_state.sw_laps: st.table(pd.DataFrame(st.session_state.sw_laps, columns=["Laps"]))

# --- TAB 3: AUTOMATIC POMODORO ---
    with tab3:
        st.subheader("🍅 Automatic Pomodoro Cycle")

        # 1. Task Selection Integration (Corrected Indentation)
        if "todo_list" in st.session_state and st.session_state.todo_list:
            # Filter for only incomplete tasks
            pending_tasks = [t["task"] for t in st.session_state.todo_list if not t["done"]]
            
            if pending_tasks:
                # We use a key here to ensure it stays synced
                current_focus = st.selectbox("🎯 Select Your Current Focus:", pending_tasks, key="p_focus_select")
                st.info(f"Currently Working On: **{current_focus}**")
            else:
                st.success("🎉 All tasks complete! Time for a break?")
        else:
            st.warning("💡 Add a task in the sidebar to track your focus here!")

        # 2. State Initialization
        if "p_active" not in st.session_state: st.session_state.p_active = False
        if "p_mode" not in st.session_state: st.session_state.p_mode = "Work"
        
        # 3. Configuration
        st.write("### Define Your Intervals")
        cfg_col1, cfg_col2 = st.columns(2)
        with cfg_col1:
            work_m = st.number_input("Work Minutes:", min_value=1, value=20, key="p_work_m")
        with cfg_col2:
            break_m = st.number_input("Break Minutes:", min_value=1, value=5, key="p_break_m")

        auto_cycle = st.toggle("Auto-Start Next Session", value=True)

        if "p_seconds_left" not in st.session_state:
            st.session_state.p_seconds_left = work_m * 60

        # 4. Controls
        st.divider()
        c1, c2, c3 = st.columns(3)
        if c1.button("▶️ Start Session", use_container_width=True, type="primary", key="p_start_btn"):
            st.session_state.p_active = True
        if c2.button("⏸️ Pause", use_container_width=True, key="p_pause_btn"):
            st.session_state.p_active = False
            st.rerun()
        if c3.button("🔄 Reset to Work", use_container_width=True, key="p_reset_btn"):
            st.session_state.p_active = False
            st.session_state.p_mode = "Work"
            st.session_state.p_seconds_left = work_m * 60
            st.rerun()

        # 5. Digital Display Setup
        status_txt = st.empty()
        p_disp = st.empty()
        
        # 6. AUTOMATIC EXECUTION LOOP
        while st.session_state.p_active:
            m, s = divmod(st.session_state.p_seconds_left, 60)
            color = "#FF4B4B" if st.session_state.p_mode == "Work" else "#00FF00"
            
            clock_html = f"""
            <div style='font-family: monospace; color: {color}; background-color: black; 
            padding: 30px; border-radius: 15px; text-align: center; font-size: 100px; 
            font-weight: bold; border: 5px solid #222;'>{int(m):02d}:{int(s):02d}</div>
            """
            
            status_txt.markdown(f"### Currently: **{st.session_state.p_mode}** Mode")
            p_disp.markdown(clock_html, unsafe_allow_html=True)
            
            time.sleep(1)
            st.session_state.p_seconds_left -= 1
            
            if st.session_state.p_seconds_left < 0:
                if auto_cycle:
                    if st.session_state.p_mode == "Work":
                        st.session_state.p_mode = "Break"
                        st.session_state.p_seconds_left = break_m * 60
                        st.toast("Work Session Over!", icon="☕")
                        st.balloons()
                    else:
                        st.session_state.p_mode = "Work"
                        st.session_state.p_seconds_left = work_m * 60
                        st.toast("Break Over!", icon="🎯")
                        st.snow()
                else:
                    st.session_state.p_active = False
                    st.rerun()

        # 7. Static Display (when paused)
        if not st.session_state.p_active:
            m, s = divmod(st.session_state.p_seconds_left, 60)
            color = "#FF4B4B" if st.session_state.p_mode == "Work" else "#00FF00"
            clock_html = f"""
            <div style='font-family: monospace; color: {color}; background-color: black; 
            padding: 30px; border-radius: 15px; text-align: center; font-size: 100px; 
            font-weight: bold; border: 5px solid #222; opacity: 0.6;'>{int(m):02d}:{int(s):02d}</div>
            """
            status_txt.markdown(f"### Paused: **{st.session_state.p_mode}**")
            p_disp.markdown(clock_html, unsafe_allow_html=True)


# --- TAB 4: DIGITAL TIMER WITH MUSIC IMPORT ---
    with tab4:
        st.subheader("⏲️ Digital Timer & Alarm Library")
        
        # 1. Music Library Section
        st.write("### 🎵 Import Alarm Music")
        uploaded_files = st.file_uploader("Upload your MP3/WAV files", type=["mp3", "wav"], accept_multiple_files=True)
        
        alarm_choice = None
        if uploaded_files:
            # Create a selection list of your uploaded songs
            song_names = [f.name for f in uploaded_files]
            selected_song_name = st.selectbox("Select Active Alarm Sound:", song_names)
            
            # Find the file object for the selected song
            for f in uploaded_files:
                if f.name == selected_song_name:
                    alarm_choice = f
            st.audio(alarm_choice) # Preview the sound
        
        st.divider()

        # 2. Timer Logic (State Management)
        if "timer_seconds" not in st.session_state: st.session_state.timer_seconds = 600
        if "timer_active" not in st.session_state: st.session_state.timer_active = False
        if "custom_presets" not in st.session_state: st.session_state.custom_presets = [60, 300]
        if "init_load" not in st.session_state: st.session_state.init_load = True
        
        # 1. Initialize State
        if "timer_seconds" not in st.session_state:
            st.session_state.timer_seconds = 600
        if "timer_active" not in st.session_state:
            st.session_state.timer_active = False
        if "custom_presets" not in st.session_state:
            # Default starting presets
            st.session_state.custom_presets = [60, 300] 
        if "init_load" not in st.session_state:
            st.session_state.init_load = True

        # 2. Main Time Setting
        st.write("### Set Your Desire")
        set_col1, set_col2 = st.columns(2)
        with set_col1:
            m_input = st.number_input("Minutes:", min_value=0, value=10, key="set_m")
        with set_col2:
            s_input = st.number_input("Seconds:", min_value=0, max_value=59, value=0, key="set_s")

        if st.session_state.init_load:
            st.session_state.timer_seconds = (m_input * 60) + s_input
            st.session_state.init_load = False

        # 3. Dynamic Quick Add Section
        st.divider()
        st.write("### Quick Add Features")
        
        # Input to create a NEW preset
        add_col1, add_col2, add_col3 = st.columns([2, 2, 1])
        with add_col1:
            new_p_m = st.number_input("Mins to Add:", min_value=0, value=1, key="new_p_m")
        with add_col2:
            new_p_s = st.number_input("Secs to Add:", min_value=0, max_value=59, value=0, key="new_p_s")
        with add_col3:
            st.write("&nbsp;") # Spacing
            if st.button("➕ Create", use_container_width=True):
                total_to_add = (new_p_m * 60) + new_p_s
                if total_to_add > 0:
                    st.session_state.custom_presets.append(total_to_add)
                    st.rerun()

        # Display the Presets as "Chips"
        st.write("**Your Timers (Click to add time, 'x' to remove):**")
        
        # Logic to display presets in a row
        if st.session_state.custom_presets:
            cols = st.columns(len(st.session_state.custom_presets))
            for i, p_total in enumerate(st.session_state.custom_presets):
                pm, ps = divmod(p_total, 60)
                label = f"+{pm}m {ps}s" if pm > 0 else f"+{ps}s"
                
                # Button to add the time
                if cols[i].button(label, key=f"use_p_{i}", use_container_width=True):
                    st.session_state.timer_seconds += p_total
                
                # Small button to delete the preset
                if cols[i].button(f"🗑️", key=f"del_p_{i}", use_container_width=True):
                    st.session_state.custom_presets.pop(i)
                    st.rerun()
        else:
            st.info("No custom timers added yet.")

        # 4. Main Controls
        st.divider()
        c1, c2, c3 = st.columns(3)
        if c1.button("▶️ Start / Resume", use_container_width=True, type="primary", key="t_start"): 
            st.session_state.timer_active = True
        if c2.button("⏸️ Pause", use_container_width=True, key="t_pause"): 
            st.session_state.timer_active = False
            st.rerun()
        if c3.button("🔄 Reset", use_container_width=True, key="t_reset_btn"):
            st.session_state.timer_active = False
            st.session_state.timer_seconds = (m_input * 60) + s_input
            st.rerun()

        # 5. Digital Display
        timer_display = st.empty()
        clock_html = """
        <div style='font-family: monospace; color: #00FF00; background-color: black; 
        padding: 30px; border-radius: 15px; text-align: center; font-size: 100px; 
        font-weight: bold; border: 5px solid #222;'>{time_str}</div>
        """

        while st.session_state.timer_active and st.session_state.timer_seconds > 0:
            tm, ts = divmod(st.session_state.timer_seconds, 60)
            timer_display.markdown(clock_html.format(time_str=f"{int(tm):02d}:{int(ts):02d}"), unsafe_allow_html=True)
            time.sleep(1)
            st.session_state.timer_seconds -= 1
# --- Inside Tab 4 Loop ---
            if st.session_state.timer_seconds <= 0:
                st.session_state.timer_active = False
                
                # TRIGGER YOUR IMPORTED MUSIC
                if alarm_choice:
                    st.success(f"🔔 Playing: {selected_song_name}")
                    st.audio(alarm_choice, autoplay=True)
                else:
                    st.warning("⏰ Time is up! (No alarm sound selected)")
                
                st.snow()
                # Note: We don't rerun immediately so the audio component stays on screen to play
                st.stop()

        if not st.session_state.timer_active:
            tm, ts = divmod(st.session_state.timer_seconds, 60)
            timer_display.markdown(clock_html.format(time_str=f"{int(tm):02d}:{int(ts):02d}"), unsafe_allow_html=True)