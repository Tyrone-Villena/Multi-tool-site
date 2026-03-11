import streamlit as st
from datetime import datetime

def run_memo_tool():
    st.title("📝 Pro Memo Pad")
    
    # Initialize States
    if "memo_content" not in st.session_state: st.session_state.memo_content = ""
    if "todo_list" not in st.session_state: st.session_state.todo_list = []

    # --- TOP ROW: MOOD & STATUS ---
    st.write("### How's the focus today?")
    m_col = st.columns(5)
    moods = {"🔥 Focus": "Focused", "☕ Break": "Resting", "🧠 Idea": "Creative", "⚠️ Urgent": "Critical", "✅ Done": "Finished"}
    
    for i, (emoji, label) in enumerate(moods.items()):
     if m_col[i].button(emoji, use_container_width=True):
        # Changed %H:%M to %I:%M %p
        now = datetime.now().strftime("%I:%M %p") 
        st.session_state.memo_content += f"\n\n--- {emoji} ({now}) ---\n"
        st.rerun()

    st.divider()

    # --- MAIN CONTENT ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("✅ Task List")
        new_task = st.text_input("New task:", placeholder="What needs doing?")
        if st.button("Add Task", use_container_width=True) and new_task:
            st.session_state.todo_list.append({"task": new_task, "done": False})
            st.rerun()

        for i, item in enumerate(st.session_state.todo_list):
            t_col1, t_col2 = st.columns([0.85, 0.15])
            is_done = t_col1.checkbox(item["task"], value=item["done"], key=f"t_{i}")
            st.session_state.todo_list[i]["done"] = is_done
            if t_col2.button("🗑️", key=f"d_{i}"):
                st.session_state.todo_list.pop(i)
                st.rerun()

    with col2:
        tab_write, tab_preview = st.tabs(["✍️ Write", "👁️ Preview"])
        
        with tab_write:
            memo_text = st.text_area(
                "Notes (Markdown supported):", 
                value=st.session_state.memo_content, 
                height=450
            )
            st.session_state.memo_content = memo_text
            
            # Action Buttons
            b1, b2, b3 = st.columns(3)
            if b1.button("🕒 Add Timestamp"):
                now_ts = datetime.now().strftime("%I:%M:%S %p")
                st.session_state.memo_content += f"\n[{now_ts}] "
                st.rerun()
            if b2.button("🧹 Clear All"):
                st.session_state.memo_content = ""
                st.rerun()
            
            # Export
            b3.download_button("💾 Save .txt", st.session_state.memo_content, file_name="memos.txt")

        with tab_preview:
            st.markdown("### Document Preview")
            st.markdown("---")
            if st.session_state.memo_content:
                st.markdown(st.session_state.memo_content)
            else:
                st.info("Start writing in the 'Write' tab to see a preview here.")