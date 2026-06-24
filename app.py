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


if not st.session_state.get("authenticated"):
    show_login()
    st.stop()

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
    st.divider()

pg = st.navigation([
    st.Page("pages/1_dashboard.py",   title="Dashboard",       icon="📊"),
    st.Page("pages/2_patients.py",    title="Pacientes",       icon="👥"),
    st.Page("pages/3_new_patient.py", title="Nuevo Paciente",  icon="➕"),
    st.Page("pages/4_campaigns.py",   title="Campañas",        icon="📣"),
    st.Page("pages/5_settings.py",    title="Configuración",   icon="⚙️"),
])
pg.run()
