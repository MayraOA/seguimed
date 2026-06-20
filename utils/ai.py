import os
import json
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
from groq import Groq

deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MESSAGE_TYPE_LABELS = {
    "followup": "seguimiento post-consulta",
    "appointment_reminder": "recordatorio de cita",
    "no_response": "paciente sin respuesta reciente",
    "campaign_christmas": "felicitación de Navidad",
    "campaign_new_year": "felicitación de Año Nuevo",
    "campaign_checkup": "invitación a control anual",
}


def generate_message(
    patient_name: str,
    diagnosis: str,
    notes: str,
    message_type: str,
    doctor_name: str,
    specialty: str,
) -> str:
    label = MESSAGE_TYPE_LABELS.get(message_type, message_type)
    system_prompt = (
        f"Eres el asistente personal del {doctor_name}, {specialty}, "
        "en Lima, Perú. Redactas mensajes de WhatsApp en español peruano."
    )
    user_prompt = (
        f"Redacta un mensaje de WhatsApp para el paciente {patient_name}. "
        f"Tipo de mensaje: {label}. "
        f"Contexto médico: {diagnosis or 'no especificado'}. "
        f"Notas: {notes or 'ninguna'}. "
        "Reglas: máximo 3 líneas, tono cálido y profesional, "
        "NO uses emojis excesivos (máximo 1), "
        "NO suenes robótico, incluye el nombre del doctor al final. "
        "Devuelve SOLO el mensaje, sin explicaciones ni comillas."
    )
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def transcribe_audio(audio_file_bytes: bytes, filename: str) -> str:
    transcription = groq_client.audio.transcriptions.create(
        file=(filename, audio_file_bytes),
        model="whisper-large-v3",
        language="es",
    )
    return transcription.text


def extract_patient_from_text(transcription: str) -> dict:
    prompt = (
        "Extrae datos de paciente médico del siguiente texto. "
        "Devuelve SOLO un JSON válido con estas claves exactas: "
        "name, phone, diagnosis, notes, next_appointment (formato YYYY-MM-DD o null). "
        "Si no se menciona algún dato, usa null. "
        f"Texto: {transcription}"
    )
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=400,
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
