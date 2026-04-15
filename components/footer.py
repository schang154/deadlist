import streamlit as st

def render_footer(last_update_str, source_name="Ministry of Justice, Taiwan"):
    st.markdown(
        f"""
        <style>
        .app-footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
            color: #666;
            font-size: 12px;
            background-color: white;
            border-top: 1px solid #e6e6e6;
            z-index: 999;
        }}
        </style>

        <div class="app-footer">
            Last update: {last_update_str} | Source: {source_name}
        </div>
        """,
        unsafe_allow_html=True
    )