import os
import json
import streamlit as st
from datetime import date
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Nuevo Paciente · SeguiMed", page_icon="🏥", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("Debes iniciar sesión primero.")
    st.page_link("app.py", label="Ir al login", icon="🔐")
    st.stop()

from utils.database import insert_patient
from utils.ai import transcribe_audio, extract_patient_from_text

doctor_name = st.session_state.get("doctor_name", os.getenv("DOCTOR_NAME", "Dr. Demo"))
specialty = st.session_state.get("doctor_specialty", os.getenv("DOCTOR_SPECIALTY", "Medicina General"))

with st.sidebar:
    st.markdown("## 🏥 SeguiMed")
    st.markdown(f"**{doctor_name}**")
    st.markdown(f"*{specialty}*")
    st.divider()
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

st.markdown("## ➕ Nuevo Paciente")

tab_manual, tab_voz = st.tabs(["📝 Registro manual", "🎙️ Nota de voz"])

with tab_manual:
    with st.form("form_manual"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez")
            phone = st.text_input("Teléfono *", value="+51", placeholder="+51987654321")
            last_contact = st.date_input("Fecha de última visita *", value=date.today())
        with col2:
            next_appt = st.date_input("Próxima cita (opcional)", value=None)
            diagnosis = st.text_input("Diagnóstico / motivo de consulta", placeholder="Ej: Diabetes tipo 2")
        notes = st.text_area("Notas adicionales", placeholder="Observaciones relevantes...")
        submitted = st.form_submit_button("💾 Guardar paciente", use_container_width=True)

        if submitted:
            if not name or not phone or phone == "+51":
                st.error("Nombre y teléfono son obligatorios.")
            else:
                data = {
                    "name": name,
                    "phone": phone,
                    "last_contact_date": str(last_contact),
                    "next_appointment": str(next_appt) if next_appt else None,
                    "diagnosis": diagnosis or None,
                    "notes": notes or None,
                    "status": "active",
                }
                result = insert_patient(data)
                if result["success"]:
                    st.success(f"✅ Paciente {name} guardado correctamente.")
                else:
                    st.error(f"Error al guardar: {result['error']}")

with tab_voz:
    st.markdown("Sube una nota de voz grabada durante o después de la consulta.")
    audio_file = st.file_uploader(
        "Archivo de audio", type=["mp3", "wav", "m4a", "ogg"], label_visibility="collapsed"
    )

    if audio_file is not None:
        st.audio(audio_file)
        if st.button("🎙️ Transcribir y extraer datos"):
            with st.spinner("Transcribiendo con Whisper..."):
                try:
                    audio_bytes = audio_file.read()
                    transcription = transcribe_audio(audio_bytes, audio_file.name)
                    st.session_state["transcription"] = transcription
                    st.success("Transcripción completada")
                    st.text_area("Transcripción", transcription, height=100)
                except Exception as e:
                    st.error(f"Error al transcribir: {e}")

            if st.session_state.get("transcription"):
                with st.spinner("Extrayendo datos del paciente con IA..."):
                    try:
                        extracted = extract_patient_from_text(st.session_state["transcription"])
                        st.session_state["extracted_patient"] = extracted
                    except Exception as e:
                        st.error(f"Error al extraer datos: {e}")
                        st.session_state["extracted_patient"] = {}

    extracted = st.session_state.get("extracted_patient")
    if extracted is not None:
        st.markdown("### Datos extraídos — confirma y edita")
        with st.form("form_voz"):
            col1, col2 = st.columns(2)
            with col1:
                name_v = st.text_input("Nombre completo *", value=extracted.get("name") or "")
                phone_v = st.text_input("Teléfono *", value=extracted.get("phone") or "+51")
                default_date = date.today()
                last_contact_v = st.date_input("Fecha de última visita *", value=default_date)
            with col2:
                na_raw = extracted.get("next_appointment")
                next_appt_v = st.date_input("Próxima cita (opcional)", value=None)
                diagnosis_v = st.text_input("Diagnóstico", value=extracted.get("diagnosis") or "")
            notes_v = st.text_area("Notas", value=extracted.get("notes") or "")
            confirm = st.form_submit_button("✅ Confirmar y guardar", use_container_width=True)

            if confirm:
                if not name_v or not phone_v or phone_v == "+51":
                    st.error("Nombre y teléfono son obligatorios.")
                else:
                    data = {
                        "name": name_v,
                        "phone": phone_v,
                        "last_contact_date": str(last_contact_v),
                        "next_appointment": str(next_appt_v) if next_appt_v else None,
                        "diagnosis": diagnosis_v or None,
                        "notes": notes_v or None,
                        "status": "active",
                    }
                    result = insert_patient(data)
                    if result["success"]:
                        st.success(f"✅ Paciente {name_v} guardado correctamente.")
                        st.session_state.pop("extracted_patient", None)
                        st.session_state.pop("transcription", None)
                    else:
                        st.error(f"Error al guardar: {result['error']}")
