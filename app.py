import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SeguiMed",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import apply_styles
apply_styles()

APP_PASSWORD = os.getenv("APP_PASSWORD", "demo1234")


def check_auth():
    if not st.session_state.get("authenticated"):
        show_login()
        st.stop()


def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🏥 SeguiMed")
        st.markdown("**CRM de pacientes para médicos independientes**")
        st.divider()
        with st.form("login_form"):
            password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
            submitted = st.form_submit_button("Ingresar", use_container_width=True)
            if submitted:
                if password == APP_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.session_state["doctor_name"] = os.getenv("DOCTOR_NAME", "Dr. Demo")
                    st.session_state["doctor_specialty"] = os.getenv("DOCTOR_SPECIALTY", "Medicina General")
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")


def setup_sidebar():
    with st.sidebar:
        st.markdown("## 🏥 SeguiMed")
        doctor = st.session_state.get("doctor_name", os.getenv("DOCTOR_NAME", "Dr. Demo"))
        specialty = st.session_state.get("doctor_specialty", os.getenv("DOCTOR_SPECIALTY", "Medicina General"))
        st.markdown(f"**{doctor}**")
        st.markdown(f"*{specialty}*")
        st.divider()
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()


if not st.session_state.get("authenticated"):
    show_login()
else:
    setup_sidebar()
    st.markdown("## 🏥 Bienvenido a SeguiMed")
    st.markdown("Usa el menú lateral para navegar entre las secciones.")
    st.info("👈 Selecciona **Dashboard** para ver el resumen de tus pacientes.")
