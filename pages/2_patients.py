import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Pacientes · SeguiMed", page_icon="🏥", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("Debes iniciar sesión primero.")
    st.page_link("app.py", label="Ir al login", icon="🔐")
    st.stop()

from utils.database import search_patients, get_all_patients, get_contacts_for_patient, update_patient
from utils.ai import generate_message
from utils.whatsapp import get_whatsapp_link

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

st.markdown("## 👥 Lista de Pacientes")

query = st.text_input("🔍 Buscar por nombre o teléfono", placeholder="Escribe para filtrar...")

if query:
    patients = search_patients(query)
else:
    patients = get_all_patients()

if not patients:
    st.info("No se encontraron pacientes.")
    st.stop()

detail_id = st.session_state.get("detail_patient_id")

if detail_id:
    patient = next((p for p in get_all_patients() if str(p["id"]) == str(detail_id)), None)
    if not patient:
        st.error("Paciente no encontrado.")
        st.session_state.pop("detail_patient_id")
        st.stop()

    if st.button("← Volver a la lista"):
        st.session_state.pop("detail_patient_id", None)
        st.rerun()

    st.markdown(f"## {patient['name']}")

    tab_info, tab_edit, tab_msg = st.tabs(["📋 Información", "✏️ Editar", "💬 Mensajes"])

    with tab_info:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Teléfono:** {patient.get('phone','—')}")
            st.markdown(f"**Diagnóstico:** {patient.get('diagnosis','—')}")
            st.markdown(f"**Última visita:** {patient.get('last_contact_date','—')}")
        with col2:
            st.markdown(f"**Próxima cita:** {patient.get('next_appointment','—')}")
            st.markdown(f"**Estado:** {patient.get('status','—')}")
            st.markdown(f"**Notas:** {patient.get('notes','—')}")

        st.markdown("### Historial de contactos")
        contacts = get_contacts_for_patient(patient["id"])
        if not contacts:
            st.caption("Sin contactos registrados.")
        else:
            for c in contacts:
                with st.expander(f"{c.get('contact_type','—')} · {c.get('created_at','')[:10]}"):
                    st.markdown(c.get("message_sent", ""))

    with tab_edit:
        from datetime import date
        with st.form("form_edit"):
            col1, col2 = st.columns(2)
            with col1:
                name_e = st.text_input("Nombre", value=patient.get("name", ""))
                phone_e = st.text_input("Teléfono", value=patient.get("phone", ""))
                lc_raw = patient.get("last_contact_date")
                lc_default = date.fromisoformat(lc_raw) if lc_raw else date.today()
                last_e = st.date_input("Última visita", value=lc_default)
            with col2:
                na_raw = patient.get("next_appointment")
                na_default = date.fromisoformat(na_raw) if na_raw else None
                next_e = st.date_input("Próxima cita", value=na_default)
                diag_e = st.text_input("Diagnóstico", value=patient.get("diagnosis", "") or "")
                status_e = st.selectbox("Estado", ["active", "inactive"], index=0 if patient.get("status") == "active" else 1)
            notes_e = st.text_area("Notas", value=patient.get("notes", "") or "")
            if st.form_submit_button("💾 Guardar cambios", use_container_width=True):
                result = update_patient(patient["id"], {
                    "name": name_e, "phone": phone_e,
                    "last_contact_date": str(last_e),
                    "next_appointment": str(next_e) if next_e else None,
                    "diagnosis": diag_e or None, "notes": notes_e or None,
                    "status": status_e,
                })
                if result["success"]:
                    st.success("✅ Cambios guardados.")
                else:
                    st.error(f"Error: {result['error']}")

    with tab_msg:
        msg_type = st.selectbox(
            "Tipo de mensaje",
            options=["followup", "appointment_reminder", "no_response"],
            format_func=lambda x: {
                "followup": "Seguimiento post-consulta",
                "appointment_reminder": "Recordatorio de cita",
                "no_response": "Sin respuesta",
            }[x],
        )
        if st.button("✨ Generar mensaje con IA"):
            with st.spinner("Generando..."):
                try:
                    msg = generate_message(
                        patient_name=patient["name"],
                        diagnosis=patient.get("diagnosis", ""),
                        notes=patient.get("notes", ""),
                        message_type=msg_type,
                        doctor_name=doctor_name,
                        specialty=specialty,
                    )
                    st.session_state["detail_msg"] = msg
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.get("detail_msg"):
            edited = st.text_area("Mensaje", value=st.session_state["detail_msg"], height=120)
            wa_link = get_whatsapp_link(patient.get("phone", ""), edited)
            st.link_button("📱 Abrir en WhatsApp", wa_link)

else:
    st.markdown(f"**{len(patients)} pacientes**")
    st.divider()

    header = st.columns([3, 2, 2, 2, 2])
    for col, label in zip(header, ["Nombre", "Teléfono", "Última visita", "Diagnóstico", "Acción"]):
        col.markdown(f"**{label}**")
    st.divider()

    for p in patients:
        cols = st.columns([3, 2, 2, 2, 2])
        cols[0].markdown(p.get("name", "—"))
        cols[1].markdown(p.get("phone", "—"))
        cols[2].markdown(p.get("last_contact_date", "—"))
        cols[3].markdown(p.get("diagnosis", "—") or "—")
        with cols[4]:
            if st.button("👁️ Ver detalle", key=f"det_{p['id']}"):
                st.session_state["detail_patient_id"] = str(p["id"])
                st.session_state.pop("detail_msg", None)
                st.rerun()
