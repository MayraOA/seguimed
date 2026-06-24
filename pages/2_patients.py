import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Pacientes · SeguiMed", page_icon="🏥", layout="wide")

from utils.styles import apply_styles
apply_styles()

if not st.session_state.get("authenticated"):
    st.warning("Debes iniciar sesión primero.")
    st.page_link("app.py", label="Ir al login", icon="🔐")
    st.stop()

from datetime import date, datetime
from utils.database import search_patients, get_all_patients, get_contacts_for_patient, update_patient
from utils.ai import generate_message
from utils.whatsapp import get_whatsapp_link
from utils.calendar import get_google_calendar_link

doctor_name = st.session_state.get("doctor_name", os.getenv("DOCTOR_NAME", "Dr. Demo"))
specialty = st.session_state.get("doctor_specialty", os.getenv("DOCTOR_SPECIALTY", "Medicina General"))

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

    tab_info, tab_edit, tab_msg, tab_hist = st.tabs(["📋 Información", "✏️ Editar", "💬 Mensajes", "📋 Historial"])

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

        st.divider()
        na = patient.get("next_appointment")
        lc = patient.get("last_contact_date")
        if na:
            try:
                cal_url = get_google_calendar_link(
                    patient["name"], date.fromisoformat(na), patient.get("diagnosis") or "", doctor_name
                )
                st.link_button("📅 Agregar próxima cita al Google Calendar", cal_url)
            except Exception:
                pass
        if lc:
            try:
                cal_url = get_google_calendar_link(
                    patient["name"], date.fromisoformat(lc), patient.get("diagnosis") or "", doctor_name
                )
                st.link_button("📅 Registrar cita pasada en Calendar", cal_url)
            except Exception:
                pass

    with tab_edit:
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

    with tab_hist:
        MONTHS_ES = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        ]
        CONTACT_ICONS = {
            "cita_pasada": "🗓️",
            "cita_futura": "📅",
            "followup": "💬",
            "whatsapp": "💬",
            "appointment_reminder": "💬",
            "no_response": "💬",
        }
        CONTACT_BADGES = {
            "cita_pasada":          ("#636363", "Cita pasada"),
            "cita_futura":          ("#0F6E56", "Cita futura"),
            "followup":             ("#1D9E75", "Seguimiento"),
            "whatsapp":             ("#25D366", "WhatsApp"),
            "appointment_reminder": ("#ffa500", "Recordatorio"),
            "no_response":          ("#ff4b4b", "Sin respuesta"),
            "campaign_christmas":   ("#c0392b", "Campaña"),
            "campaign_new_year":    ("#8e44ad", "Campaña"),
            "campaign_checkup":     ("#2980b9", "Campaña"),
        }

        contacts = get_contacts_for_patient(patient["id"])
        if not contacts:
            st.info("No hay registros de contacto aún.")
        else:
            for c in contacts:
                ct = c.get("contact_type", "")
                icon = "📣" if ct.startswith("campaign") else CONTACT_ICONS.get(ct, "📌")
                badge_color, badge_label = CONTACT_BADGES.get(ct, ("#555555", ct.replace("_", " ").title()))

                raw_dt = c.get("created_at", "")
                try:
                    dt_obj = datetime.fromisoformat(raw_dt[:19])
                    formatted_date = f"{dt_obj.day} de {MONTHS_ES[dt_obj.month - 1]} de {dt_obj.year}"
                except Exception:
                    formatted_date = raw_dt[:10] if raw_dt else "—"

                col_icon, col_body = st.columns([1, 11])
                with col_icon:
                    st.markdown(
                        f"<div style='font-size:22px;padding-top:6px'>{icon}</div>",
                        unsafe_allow_html=True,
                    )
                with col_body:
                    st.markdown(
                        f"**{formatted_date}** &nbsp;"
                        f'<span style="background:{badge_color};color:white;'
                        f'padding:2px 10px;border-radius:4px;font-size:12px">{badge_label}</span>',
                        unsafe_allow_html=True,
                    )
                    st.caption(c.get("message_sent", ""))

                    if ct in ("cita_pasada", "cita_futura"):
                        try:
                            msg = c.get("message_sent", "")
                            date_str = msg.split("Cita registrada: ")[1].split(" —")[0].strip()
                            cal_dt = date.fromisoformat(date_str)
                            cal_url = get_google_calendar_link(
                                patient["name"], cal_dt,
                                patient.get("diagnosis") or "", doctor_name,
                            )
                            st.link_button("Ver en Google Calendar", cal_url, key=f"hist_cal_{c.get('id','')}")
                        except Exception:
                            pass

                st.divider()

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
