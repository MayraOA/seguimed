import os
import json
import streamlit as st
from datetime import date
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Nuevo Paciente · SeguiMed", page_icon="🏥", layout="wide")

from utils.styles import apply_styles
apply_styles()

if not st.session_state.get("authenticated"):
    st.warning("Debes iniciar sesión primero.")
    st.page_link("app.py", label="Ir al login", icon="🔐")
    st.stop()

from utils.database import insert_patient
from utils.ai import transcribe_audio, extract_patient_from_text
from utils.calendar import get_google_calendar_link

doctor_name = st.session_state.get("doctor_name", os.getenv("DOCTOR_NAME", "Dr. Demo"))
specialty = st.session_state.get("doctor_specialty", os.getenv("DOCTOR_SPECIALTY", "Medicina General"))

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
                    st.session_state["saved_manual"] = {
                        "name": name,
                        "next_appointment": str(next_appt) if next_appt else None,
                        "last_contact_date": str(last_contact),
                        "diagnosis": diagnosis or "",
                    }
                else:
                    st.error(f"Error al guardar: {result['error']}")
                    st.session_state.pop("saved_manual", None)

    saved_m = st.session_state.get("saved_manual")
    if saved_m:
        st.markdown("**📅 Agregar al Google Calendar**")
        na = saved_m.get("next_appointment")
        lc = saved_m.get("last_contact_date")
        if na:
            try:
                cal_url = get_google_calendar_link(
                    saved_m["name"], date.fromisoformat(na), saved_m["diagnosis"], doctor_name
                )
                st.link_button(f"📅 Agendar próxima cita ({na})", cal_url, key="cal_m_na")
            except Exception:
                pass
        if lc:
            try:
                cal_url = get_google_calendar_link(
                    saved_m["name"], date.fromisoformat(lc), saved_m["diagnosis"], doctor_name
                )
                st.link_button(f"📅 Registrar cita anterior ({lc})", cal_url, key="cal_m_lc")
            except Exception:
                pass

with tab_voz:
    st.markdown("Graba o sube una nota de voz para registrar al paciente automáticamente.")

    input_mode = st.radio(
        "modo",
        ["🎙️ Grabar ahora", "📁 Subir archivo"],
        horizontal=True,
        label_visibility="collapsed",
    )

    audio_data = None
    audio_filename = "recording.wav"

    if input_mode == "🎙️ Grabar ahora":
        recorded = st.audio_input("🎙️ Grabar nota de voz")
        if recorded:
            audio_data = recorded
    else:
        uploaded = st.file_uploader(
            "Archivo de audio", type=["mp3", "wav", "m4a", "ogg"], label_visibility="collapsed"
        )
        if uploaded:
            audio_data = uploaded
            audio_filename = uploaded.name

    if audio_data is not None:
        st.audio(audio_data)
        st.divider()

        if st.button("🔍 Transcribir y extraer datos", type="primary"):
            audio_bytes = audio_data.read()
            with st.spinner("Transcribiendo con Whisper..."):
                try:
                    transcription = transcribe_audio(audio_bytes, audio_filename)
                    st.session_state["transcription"] = transcription
                    st.session_state.pop("extracted_patient", None)
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

    if st.session_state.get("transcription"):
        with st.expander("📝 Ver transcripción completa"):
            st.text(st.session_state["transcription"])

    extracted = st.session_state.get("extracted_patient")
    if extracted is not None:
        st.markdown("### Datos extraídos — confirma y edita")
        with st.form("form_voz"):
            col1, col2 = st.columns(2)
            with col1:
                name_v = st.text_input("Nombre completo *", value=extracted.get("name") or "")
                phone_v = st.text_input("Teléfono *", value=extracted.get("phone") or "+51")
                last_contact_v = st.date_input("Fecha de última visita *", value=date.today())
            with col2:
                next_appt_v = st.date_input("Próxima cita (opcional)", value=None)
                diagnosis_v = st.text_input("Diagnóstico", value=extracted.get("diagnosis") or "")
            notes_v = st.text_area("Notas", value=extracted.get("notes") or "")
            confirm = st.form_submit_button("✅ Confirmar y guardar paciente", use_container_width=True)

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
                        st.session_state["saved_voz"] = {
                            "name": name_v,
                            "next_appointment": str(next_appt_v) if next_appt_v else None,
                            "last_contact_date": str(last_contact_v),
                            "diagnosis": diagnosis_v or "",
                        }
                    else:
                        st.error(f"Error al guardar: {result['error']}")
                        st.session_state.pop("saved_voz", None)

    saved_v = st.session_state.get("saved_voz")
    if saved_v:
        st.markdown("**📅 Agregar al Google Calendar**")
        na = saved_v.get("next_appointment")
        lc = saved_v.get("last_contact_date")
        if na:
            try:
                cal_url = get_google_calendar_link(
                    saved_v["name"], date.fromisoformat(na), saved_v["diagnosis"], doctor_name
                )
                st.link_button(f"📅 Agendar próxima cita ({na})", cal_url, key="cal_v_na")
            except Exception:
                pass
        if lc:
            try:
                cal_url = get_google_calendar_link(
                    saved_v["name"], date.fromisoformat(lc), saved_v["diagnosis"], doctor_name
                )
                st.link_button(f"📅 Registrar cita anterior ({lc})", cal_url, key="cal_v_lc")
            except Exception:
                pass
