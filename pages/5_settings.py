import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Configuración · SeguiMed", page_icon="🏥", layout="wide")

from utils.styles import apply_styles
apply_styles()

if not st.session_state.get("authenticated"):
    st.warning("Debes iniciar sesión primero.")
    st.page_link("app.py", label="Ir al login", icon="🔐")
    st.stop()

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.json")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(data: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


doctor_name = st.session_state.get("doctor_name", os.getenv("DOCTOR_NAME", "Dr. Demo"))
specialty = st.session_state.get("doctor_specialty", os.getenv("DOCTOR_SPECIALTY", "Medicina General"))

st.markdown("## ⚙️ Configuración")

saved = load_config()
current_name = saved.get("doctor_name", doctor_name)
current_specialty = saved.get("doctor_specialty", specialty)

with st.form("settings_form"):
    new_name = st.text_input("Nombre del doctor", value=current_name)
    new_specialty = st.text_input("Especialidad", value=current_specialty)
    submitted = st.form_submit_button("💾 Guardar configuración", use_container_width=True)

    if submitted:
        if not new_name:
            st.error("El nombre no puede estar vacío.")
        else:
            st.session_state["doctor_name"] = new_name
            st.session_state["doctor_specialty"] = new_specialty
            save_config({"doctor_name": new_name, "doctor_specialty": new_specialty})
            st.success("✅ Configuración guardada.")

st.markdown("---")
preview_name = st.session_state.get("doctor_name", current_name)
preview_spec = st.session_state.get("doctor_specialty", current_specialty)
st.info(f"Los mensajes se firmarán como: **{preview_name}**, *{preview_spec}*")
