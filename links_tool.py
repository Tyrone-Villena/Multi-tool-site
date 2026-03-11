import streamlit as st

def run_links_tool():
    st.title("🚀 Quick Link Dashboard")

    # 1. Initialize Link Storage
    if "my_links" not in st.session_state:
        st.session_state.my_links = {
            "Google": "https://www.google.com",
            "GitHub": "https://www.github.com",
            "YouTube": "https://www.youtube.com",
            "ChatGPT": "https://chat.openai.com",
            "Canva": "https://www.canva.com",
            "Gemini": "https://gemini.google.com"
        }

    # 2. MANAGEMENT SECTION
    with st.expander("🛠️ Manage Shortcuts"):
        add_col1, add_col2 = st.columns(2)
        new_name = add_col1.text_input("Site Name:", placeholder="e.g. Netflix")
        new_url = add_col2.text_input("URL:", placeholder="https://...")
        
        if st.button("➕ Save to Dashboard", use_container_width=True):
            if new_name and new_url:
                # Ensure URL has https://
                if not new_url.startswith("http"):
                    new_url = "https://" + new_url
                st.session_state.my_links[new_name] = new_url
                st.rerun()
        
        st.divider()
        for name in list(st.session_state.my_links.keys()):
            del_col1, del_col2 = st.columns([0.8, 0.2])
            del_col1.write(f"🔗 {name}")
            if del_col2.button("🗑️", key=f"del_{name}"):
                del st.session_state.my_links[name]
                st.rerun()

    st.divider()

    # 3. THE BRANDED GRID
    cols = st.columns(4)
    
    for i, (name, url) in enumerate(st.session_state.my_links.items()):
        # Fetch Favicon via Google API
        favicon_url = f"https://www.google.com/s2/favicons?domain={url}&sz=64"
        
        with cols[i % 4]:
            # Custom HTML for a "Pro" Button Look
            st.markdown(
                f"""
                <a href="{url}" target="_blank" style="text-decoration: none;">
                    <div style="
                        background-color: #f0f2f6;
                        border-radius: 10px;
                        padding: 15px;
                        text-align: center;
                        border: 1px solid #ddd;
                        transition: 0.3s;
                        margin-bottom: 10px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        gap: 10px;
                    ">
                        <img src="{favicon_url}" width="32" height="32" style="border-radius: 4px;">
                        <span style="color: #31333F; font-weight: bold; font-family: sans-serif;">{name}</span>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )

    st.info("💡 Icons are automatically fetched from the website URLs.")