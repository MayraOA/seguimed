import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        [data-testid="stFooter"], #MainMenu, footer {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            background-color: #083D2C !important;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: #0F6E56 !important;
            border: 1px solid #1D9E75 !important;
        }

        .stButton > button[kind="primary"] {
            background-color: #0F6E56 !important;
            border-radius: 8px !important;
            border: none !important;
        }

        [data-testid="metric-container"] {
            border-left: 4px solid #0F6E56;
            padding-left: 12px;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
