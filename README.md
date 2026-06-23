# 🏥 SeguiMed

> **CRM inteligente para médicos independientes en Latinoamérica que automatiza el seguimiento de pacientes por WhatsApp con IA.**

[![CI](https://github.com/MayraOA/seguimed/actions/workflows/ci.yml/badge.svg)](https://github.com/MayraOA/seguimed/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.35+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Demo en vivo

**URL:** [https://seguimed.streamlit.app](https://seguimed.streamlit.app)  
**Contraseña:** `demo1234`

---

## El problema (validado con 5 entrevistas)

Los médicos independientes en Lima manejan 80-200 pacientes activos únicamente por WhatsApp personal, sin asistente ni CRM. El problema no es que no respondan — **5 de 5 médicos entrevistados responden todos sus mensajes**. El problema es que nadie inicia el contacto cuando el paciente desaparece.

| Hallazgo | Dato |
|---|---|
| Médicos que perdieron pacientes | 3 de 5 confirmado |
| Horas/semana que invierte el que no pierde pacientes | ~20 horas |
| Médicos con CRM dedicado | 0 de 5 |
| Precio validado espontáneamente | S/.50/mes (E5) |
| Sistema previo que intentaron | Falló porque requería que el **paciente** cambiara su comportamiento |

> *"Ya tuve experiencia con un sistema, pero no funcionó porque varios de mis pacientes no sabían usarlo."* — Médico entrevistado, Lima 2026

**SeguiMed resuelve esto:** solo el médico cambia su flujo. Los pacientes siguen recibiendo WhatsApp normal.

Ver evidencia completa en [`docs/research/`](docs/research/).

---

## La solución

Dashboard priorizado + IA que genera el mensaje + link de WhatsApp prellenado. El médico toca "Enviar" — 10 segundos total.

**Funcionalidades del MVP:**
- Dashboard con 4 métricas de estado de pacientes en tiempo real
- Generación de mensajes personalizados por IA en español peruano
- Links de WhatsApp con mensaje prellenado (1 clic)
- Registro de pacientes por nota de voz (Whisper transcribe → IA extrae datos)
- Campañas de temporada para toda la base de pacientes (Navidad, Año Nuevo, control anual)

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   MÉDICO (browser)                  │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────┐
│           Streamlit App (Frontend + Backend)         │
│                                                      │
│  pages/1_dashboard.py   → métricas + tabla priorizada│
│  pages/2_patients.py    → lista, búsqueda, detalle   │
│  pages/3_new_patient.py → alta manual + por voz      │
│  pages/4_campaigns.py   → campañas masivas           │
│  pages/5_settings.py    → configuración del médico   │
└──────┬───────────────┬───────────────┬───────────────┘
       │               │               │
┌──────▼──────┐ ┌──────▼──────┐ ┌─────▼──────────────┐
│  Supabase   │ │ DeepSeek-V3 │ │ Groq Whisper v3    │
│ PostgreSQL  │ │     API     │ │       API          │
│             │ │             │ │                    │
│ patients    │ │ Generación  │ │ Transcripción      │
│ contacts    │ │ de mensajes │ │ de audio en        │
│             │ │ en español  │ │ español            │
└─────────────┘ └─────────────┘ └────────────────────┘
                       │
              ┌────────▼────────┐
              │   WhatsApp      │
              │  deep links     │
              │ wa.me/{phone}   │
              │ ?text={mensaje} │
              └─────────────────┘

Deploy: Streamlit Community Cloud (gratuito)
CI/CD:  GitHub Actions (flake8 lint)
```

---

## Herramientas de IA del curso utilizadas

| Herramienta | Dónde en el código | Por qué |
|---|---|---|
| **DeepSeek-V3** | `utils/ai.py` → `generate_message()`, `extract_patient_from_text()` | Generación de mensajes personalizados en español peruano. Costo: $0.001/mensaje — 100x más barato que GPT-4o. Mismo formato de API que OpenAI. |
| **Whisper large-v3** (via Groq) | `utils/ai.py` → `transcribe_audio()` | Transcripción de notas de voz del médico para registro de pacientes. Tier gratuito, latencia <2 s, precisión casi perfecta en español. |

---

## Stack técnico

| Componente | Tecnología |
|---|---|
| Frontend + Backend | Streamlit (Python) |
| Base de datos | Supabase (PostgreSQL) |
| IA — mensajes | DeepSeek-V3 |
| IA — voz | Whisper large-v3 via Groq |
| Deploy | Streamlit Community Cloud |
| CI/CD | GitHub Actions (flake8) |

---

## Estructura del repositorio

```
seguimed/
├── app.py                      # Entry point: login, sidebar, navegación
├── pages/
│   ├── 1_dashboard.py          # Dashboard: 4 métricas + tabla priorizada
│   ├── 2_patients.py           # Lista, búsqueda y detalle de pacientes
│   ├── 3_new_patient.py        # Alta manual + registro por nota de voz
│   ├── 4_campaigns.py          # Campañas masivas de temporada
│   └── 5_settings.py           # Nombre y especialidad del médico
├── utils/
│   ├── ai.py                   # DeepSeek-V3 + Groq Whisper
│   ├── database.py             # CRUD Supabase + fallback demo
│   ├── styles.py               # CSS personalizado del brand
│   └── whatsapp.py             # Generador de links wa.me
├── docs/
│   ├── seguimed_pitch.pptx     # Pitch deck completo (12 slides)
│   ├── pitch_deck.md           # Dossier YC-format completo
│   ├── screenshots/            # Capturas del flujo principal
│   ├── brand/                  # Logo SVG e ícono
│   └── research/               # 5 entrevistas + resumen de hallazgos
├── .streamlit/
│   └── config.toml             # Tema visual SeguiMed
├── .github/
│   └── workflows/ci.yml        # CI: flake8 lint
├── requirements.txt
├── .env.example
└── LICENSE
```

---

## Setup local

### 1. Clonar el repositorio

```bash
git clone https://github.com/MayraOA/seguimed.git
cd seguimed
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus keys reales
```

Variables necesarias:

```env
DEEPSEEK_API_KEY=        # platform.deepseek.com
GROQ_API_KEY=            # console.groq.com (gratis)
SUPABASE_URL=            # Project URL de Supabase
SUPABASE_KEY=            # Publishable key de Supabase
DOCTOR_NAME=Dr. Demo
DOCTOR_SPECIALTY=Medicina General
APP_PASSWORD=demo1234
```

### 4. Crear tablas en Supabase

En el SQL Editor de tu proyecto Supabase:

```sql
create table patients (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp default now(),
  name text not null,
  phone text not null,
  last_contact_date date,
  next_appointment date,
  diagnosis text,
  notes text,
  status text default 'active'
);

create table contacts (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp default now(),
  patient_id uuid references patients(id) on delete cascade,
  message_sent text,
  contact_type text
);
```

### 5. Correr la app

```bash
streamlit run app.py
```

La app abre en `http://localhost:8501`. Contraseña: `demo1234`.

> **Modo demo:** Si Supabase no está configurado, la app carga automáticamente 5 pacientes ficticios para explorar las funcionalidades.

---

## Modelo de negocio

| Plan | Precio | Límite |
|---|---|---|
| Básico | S/.49/mes | 100 pacientes |
| Pro | S/.99/mes | 500 pacientes + campañas |
| Clínica | S/.199/mes | Ilimitado + multi-usuario |

**Contribution margin: ~99%** — Costo variable por usuario: S/.0.50/mes (DeepSeek + hosting).

---

## Validación de mercado

**5 entrevistas** con médicos independientes en Lima Metropolitana — Junio 2026.

Ver carpeta [`docs/research/`](docs/research/) para entrevistas individuales y resumen de hallazgos.

**Mercado:**
- TAM: $288M/año (800K médicos independientes en LatAm × $30/mes — OPS)
- SAM: S/.19M/año (20K médicos en Perú con gestión por WhatsApp — CMP 2024)
- SOM: S/.474K/año (500 usuarios en Lima en primeros 12 meses)

---

## Autora

**Mayra Otiniano Alvarado**  
Universidad del Pacífico — Data Science con Python 2026-I  
Proyecto Final — Solo Founder

---

*Construido con Claude Code, DeepSeek-V3 y Whisper en 11 días.*
