import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Dashboard · SeguiMed", page_icon="🏥", layout="wide")

from utils.styles import apply_styles
apply_styles()

if not st.session_state.get("authenticated"):
    st.warning("Debes iniciar sesión primero.")
    st.page_link("app.py", label="Ir al login", icon="🔐")
    st.stop()

from datetime import date
from utils.database import get_dashboard_stats, log_contact
from utils.ai import generate_message
from utils.whatsapp import get_whatsapp_link
from utils.calendar import get_google_calendar_link

doctor_name = st.session_state.get("doctor_name", os.getenv("DOCTOR_NAME", "Dr. Demo"))
specialty = st.session_state.get("doctor_specialty", os.getenv("DOCTOR_SPECIALTY", "Medicina General"))

st.markdown("## 📊 Dashboard")

with st.spinner("Cargando datos..."):
    stats = get_dashboard_stats()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""<div style="background:#fff0f0;padding:16px;border-radius:10px;border-left:4px solid #ff4b4b">
        <div style="font-size:28px;font-weight:bold;color:#ff4b4b">{stats['no_contact_7']}</div>
        <div style="color:#555;font-size:13px">🔴 Sin contacto +7 días</div></div>""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""<div style="background:#fff8f0;padding:16px;border-radius:10px;border-left:4px solid #ffa500">
        <div style="font-size:28px;font-weight:bold;color:#ffa500">{stats['appt_this_week']}</div>
        <div style="color:#555;font-size:13px">🟡 Cita esta semana</div></div>""",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""<div style="background:#f5f5f5;padding:16px;border-radius:10px;border-left:4px solid #888888">
        <div style="font-size:28px;font-weight:bold;color:#888888">{stats['inactive_30']}</div>
        <div style="color:#555;font-size:13px">⚪ Inactivos +30 días</div></div>""",
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f"""<div style="background:#f0fff4;padding:16px;border-radius:10px;border-left:4px solid #00cc44">
        <div style="font-size:28px;font-weight:bold;color:#00cc44">{stats['total_active']}</div>
        <div style="color:#555;font-size:13px">📊 Pacientes activos</div></div>""",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("### 👥 Pacientes priorizados")
st.caption("Ordenados por días sin contacto (mayor a menor)")

patients = stats["prioritized"]

if not patients:
    st.info("No hay pacientes registrados aún.")
else:
    for p in patients:
        days = p.get("_days_since", 0)
        if days >= 30:
            badge = f'<span style="color:#888888">⚪ {days}d sin contacto</span>'
        elif days >= 7:
            badge = f'<span style="color:#ff4b4b">🔴 {days}d sin contacto</span>'
        else:
            badge = f'<span style="color:#00cc44">🟢 {days}d sin contacto</span>'

        with st.container():
            c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
            with c1:
                st.markdown(f"**{p['name']}**")
            with c2:
                st.markdown(p.get("phone", "—"))
            with c3:
                lc = p.get("last_contact_date", "—")
                st.markdown(lc)
            with c4:
                st.markdown(badge, unsafe_allow_html=True)
            with c5:
                if st.button("💬 Generar mensaje", key=f"gen_{p['id']}"):
                    st.session_state[f"show_msg_{p['id']}"] = True

        if st.session_state.get(f"show_msg_{p['id']}"):
            with st.expander(f"Mensaje para {p['name']}", expanded=True):
                msg_type = st.selectbox(
                    "Tipo de mensaje",
                    options=["followup", "appointment_reminder", "no_response"],
                    format_func=lambda x: {
                        "followup": "Seguimiento post-consulta",
                        "appointment_reminder": "Recordatorio de cita",
                        "no_response": "Sin respuesta",
                    }[x],
                    key=f"type_{p['id']}",
                )
                if st.button("✨ Generar con IA", key=f"ai_{p['id']}"):
                    with st.spinner("Generando mensaje..."):
                        try:
                            msg = generate_message(
                                patient_name=p["name"],
                                diagnosis=p.get("diagnosis", ""),
                                notes=p.get("notes", ""),
                                message_type=msg_type,
                                doctor_name=doctor_name,
                                specialty=specialty,
                            )
                            st.session_state[f"msg_text_{p['id']}"] = msg
                            log_contact(p["id"], msg, "whatsapp")
                        except Exception as e:
                            st.error(f"Error al generar: {e}")

                msg_text = st.session_state.get(f"msg_text_{p['id']}", "")
                if msg_text:
                    edited = st.text_area("Mensaje generado (editable)", value=msg_text, key=f"edited_{p['id']}", height=120)
                    wa_link = get_whatsapp_link(p.get("phone", ""), edited)
                    st.link_button("📱 Abrir en WhatsApp", wa_link)

                na = p.get("next_appointment")
                lc = p.get("last_contact_date")
                if na:
                    try:
                        cal_url = get_google_calendar_link(
                            p["name"], date.fromisoformat(na), p.get("diagnosis") or "", doctor_name
                        )
                        st.link_button("📅 Agregar próxima cita al Google Calendar", cal_url, key=f"cal_na_{p['id']}")
                    except Exception:
                        pass
                elif lc:
                    try:
                        cal_url = get_google_calendar_link(
                            p["name"], date.fromisoformat(lc), p.get("diagnosis") or "", doctor_name
                        )
                        st.link_button("📅 Registrar cita pasada en Calendar", cal_url, key=f"cal_lc_{p['id']}")
                    except Exception:
                        pass

        st.divider()
