import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Campañas · SeguiMed", page_icon="🏥", layout="wide")

from utils.styles import apply_styles
apply_styles()

if not st.session_state.get("authenticated"):
    st.warning("Debes iniciar sesión primero.")
    st.page_link("app.py", label="Ir al login", icon="🔐")
    st.stop()

from utils.database import get_all_patients
from utils.ai import generate_message
from utils.whatsapp import get_whatsapp_link

doctor_name = st.session_state.get("doctor_name", os.getenv("DOCTOR_NAME", "Dr. Demo"))
specialty = st.session_state.get("doctor_specialty", os.getenv("DOCTOR_SPECIALTY", "Medicina General"))

st.markdown("## 📣 Campañas Masivas")

CAMPAIGN_OPTIONS = {
    "campaign_christmas": "🎄 Felicitación Navidad",
    "campaign_new_year": "🎆 Felicitación Año Nuevo",
    "campaign_checkup": "🩺 Invitación a control anual",
}

campaign_type = st.selectbox(
    "Tipo de campaña",
    options=list(CAMPAIGN_OPTIONS.keys()),
    format_func=lambda x: CAMPAIGN_OPTIONS[x],
)

patients = [p for p in get_all_patients() if p.get("status") == "active"]

if not patients:
    st.info("No hay pacientes activos.")
    st.stop()

if st.button("👁️ Generar preview del mensaje"):
    first = patients[0]
    with st.spinner("Generando preview..."):
        try:
            preview = generate_message(
                patient_name=first["name"],
                diagnosis=first.get("diagnosis", ""),
                notes=first.get("notes", ""),
                message_type=campaign_type,
                doctor_name=doctor_name,
                specialty=specialty,
            )
            st.session_state["campaign_preview"] = preview
            st.session_state["campaign_preview_name"] = first["name"]
        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.get("campaign_preview"):
    st.markdown("**Preview (basado en primer paciente):**")
    st.info(f"*{st.session_state['campaign_preview_name']}:* {st.session_state['campaign_preview']}")

st.markdown("---")
st.markdown("### Selecciona destinatarios")

select_all = st.checkbox("Seleccionar todos")

selected_ids = []
for p in patients:
    checked = st.checkbox(f"{p['name']} · {p.get('phone','—')} · {p.get('diagnosis','—') or '—'}", value=select_all, key=f"chk_{p['id']}")
    if checked:
        selected_ids.append(p["id"])

st.markdown(f"**{len(selected_ids)} pacientes seleccionados**")

if st.button("🚀 Generar links de WhatsApp", disabled=len(selected_ids) == 0):
    selected_patients = [p for p in patients if p["id"] in selected_ids]
    with st.spinner(f"Generando {len(selected_patients)} mensajes..."):
        links = []
        errors = []
        for p in selected_patients:
            try:
                msg = generate_message(
                    patient_name=p["name"],
                    diagnosis=p.get("diagnosis", ""),
                    notes=p.get("notes", ""),
                    message_type=campaign_type,
                    doctor_name=doctor_name,
                    specialty=specialty,
                )
                link = get_whatsapp_link(p.get("phone", ""), msg)
                links.append({"patient": p, "msg": msg, "link": link})
            except Exception as e:
                errors.append(f"{p['name']}: {e}")

    if errors:
        st.warning(f"Errores en {len(errors)} pacientes: {'; '.join(errors)}")

    st.markdown(f"### ✅ {len(links)} links generados")
    for item in links:
        col1, col2 = st.columns([4, 2])
        with col1:
            st.markdown(f"**{item['patient']['name']}** · {item['patient'].get('phone','—')}")
            st.caption(item["msg"])
        with col2:
            st.link_button("📱 WhatsApp", item["link"])
        st.divider()
