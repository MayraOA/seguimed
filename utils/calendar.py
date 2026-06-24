from urllib.parse import quote
from datetime import date as date_type


def get_google_calendar_link(
    patient_name: str,
    dt: date_type,
    diagnosis: str,
    doctor_name: str,
) -> str:
    date_str = dt.strftime("%Y%m%d")
    base = "https://calendar.google.com/calendar/render?action=TEMPLATE"
    text = f"Cita: {patient_name} - {doctor_name}"
    details = f"Diagnóstico/motivo: {diagnosis or 'No especificado'}"
    return f"{base}&text={quote(text)}&dates={date_str}/{date_str}&details={quote(details)}"
