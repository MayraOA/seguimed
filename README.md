# 🏥 SeguiMed

CRM de pacientes con IA para médicos independientes en Latinoamérica.

## El problema

Los médicos independientes con 50-200 pacientes pierden pacientes por falta de seguimiento. No tienen asistente, gestionan todo por WhatsApp, y no tienen visibilidad de quién necesita atención.

## La solución

SeguiMed les da un dashboard simple donde ven quién necesita atención y pueden generar mensajes de WhatsApp personalizados con IA en segundos.

## Demo

🔗 [Demo en Streamlit Cloud](https://seguimed.streamlit.app) *(placeholder)*

Contraseña demo: `demo1234`

---

## Setup local

### 1. Clonar el repo

```bash
git clone https://github.com/tu-usuario/seguimed.git
cd seguimed
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

| Variable | Descripción |
|---|---|
| `DEEPSEEK_API_KEY` | API key de DeepSeek (platform.deepseek.com) |
| `GROQ_API_KEY` | API key de Groq (console.groq.com) |
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_KEY` | Clave pública (anon) de Supabase |
| `DOCTOR_NAME` | Nombre del doctor (ej: Dr. García) |
| `DOCTOR_SPECIALTY` | Especialidad (ej: Cardiología) |
| `APP_PASSWORD` | Contraseña de acceso a la app |

### 5. Tablas en Supabase

Crea las siguientes tablas en tu proyecto Supabase:

```sql
create table patients (
  id uuid default gen_random_uuid() primary key,
  created_at timestamptz default now(),
  name text not null,
  phone text,
  last_contact_date date,
  next_appointment date,
  diagnosis text,
  notes text,
  status text default 'active'
);

create table contacts (
  id uuid default gen_random_uuid() primary key,
  created_at timestamptz default now(),
  patient_id uuid references patients(id),
  message_sent text,
  contact_type text default 'whatsapp'
);
```

### 6. Ejecutar

```bash
streamlit run app.py
```

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   MÉDICO (usuario)                   │
│              Navegador / Streamlit UI                │
└──────────────┬──────────────────────┬───────────────┘
               │                      │
     ┌─────────▼──────────┐  ┌───────▼────────┐
     │   Supabase (DB)    │  │   DeepSeek V3  │
     │  patients/contacts │  │  Mensajes con  │
     │   PostgreSQL       │  │  IA en español │
     └────────────────────┘  └───────┬────────┘
                                     │
                             ┌───────▼────────┐
                             │  Groq Whisper  │
                             │  large-v3      │
                             │  Transcripción │
                             │  de voz        │
                             └────────────────┘
                                     │
                             ┌───────▼────────┐
                             │   WhatsApp     │
                             │  wa.me links   │
                             └────────────────┘
```

---

## Herramientas de IA

- **DeepSeek-V3** (`deepseek-chat`): Genera mensajes de WhatsApp personalizados en español peruano según el tipo de seguimiento y el contexto médico del paciente.
- **Whisper large-v3 via Groq**: Transcribe notas de voz del médico en tiempo real para registrar pacientes sin escribir.

---

## Estructura de carpetas

```
seguimed/
├── app.py                  # Login + página de inicio
├── pages/
│   ├── 1_dashboard.py      # Métricas + pacientes priorizados
│   ├── 2_patients.py       # Lista y detalle de pacientes
│   ├── 3_new_patient.py    # Alta manual o por nota de voz
│   ├── 4_campaigns.py      # Mensajes masivos por WhatsApp
│   └── 5_settings.py       # Configuración del doctor
├── utils/
│   ├── database.py         # CRUD Supabase + modo demo
│   ├── ai.py               # DeepSeek + Groq Whisper
│   └── whatsapp.py         # Generador de links wa.me
├── requirements.txt
├── .env.example
└── README.md
```

---

## Deploy en Streamlit Community Cloud

1. Sube el repositorio a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta el repo y selecciona `app.py` como entry point
4. En **Secrets**, agrega las variables del `.env`

---

## Contribuir

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/mi-feature`
3. Commit: `git commit -m "Add: descripción"`
4. Push: `git push origin feature/mi-feature`
5. Abre un Pull Request
