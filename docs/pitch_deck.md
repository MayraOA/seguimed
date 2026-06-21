# SeguiMed — Pitch Deck (Formato Y Combinator)

## 1. One-liner

> **SeguiMed convierte WhatsApp en un CRM inteligente para médicos independientes en Latinoamérica, usando IA para automatizar el seguimiento de sus pacientes.**

---

## 2. Founder

**Nombre:** Mayra Otiniano Alvarado  
**Universidad:** Universidad del Pacífico — Data Science con Python (2026-I)  
**Contacto:** [tu email] · [LinkedIn] · GitHub: [MayraOA](https://github.com/MayraOA)

**¿Por qué yo?**  
Tengo acceso directo al segmento objetivo (familiar médico independiente en Lima), formación en las herramientas exactas que el producto necesita (LLMs, OCR, agentes de IA, despliegue en la nube), y la capacidad de construir el producto completo como solo founder apoyada en agentes de código.

**Cómo cubro los roles clásicos como solo founder:**
- **Producto e ingeniería:** Claude Code como CTO virtual — construyó el 80% del código base
- **IA / datos:** DeepSeek-V3 para generación de mensajes, Whisper (Groq) para transcripción de voz
- **Diseño:** Sistema de diseño propio con paleta teal + ámbar, componentes Streamlit personalizados
- **Distribución:** Red médica directa a través de contacto familiar en el segmento

---

## 3. Problema

**Segmento específico:** Médicos independientes en Lima que atienden en 1-3 consultorios sin asistente administrativo propio — especialidades como traumatología, nutrición, dermatología, psicología y medicina general.

**¿Qué tan doloroso es?**
- Un médico independiente maneja entre 80-200 pacientes activos únicamente por WhatsApp personal
- Pierde entre 5-10 mensajes sin responder por semana
- No tiene sistema para recordar controles pendientes, post-operatorios o pacientes inactivos
- Cada paciente perdido equivale a S/. 80-300 en consultas no realizadas
- Trabaja en múltiples clínicas: sus pacientes lo siguen a él, no a la institución

**¿Cómo lo resuelven hoy sin SeguiMed?**
- Excel o libretas físicas para anotar pacientes
- Memoria propia para recordar seguimientos
- WhatsApp como única herramienta de comunicación y "CRM"
- Resultado: pérdida silenciosa de pacientes y relaciones de largo plazo

**Evidencia de validación:**  
*(Completar con citas textuales de las 5 entrevistas — ver `docs/research/`)*

---

## 4. Solución & Insight

**¿Qué construimos?**  
Un CRM mínimo con IA que vive en el navegador. El médico registra pacientes (manual o por nota de voz), ve un dashboard priorizado con quién necesita contacto hoy, y genera el mensaje de WhatsApp personalizado con un clic. No aprende software nuevo — sigue usando WhatsApp, pero con inteligencia detrás.

**El insight no obvio:**  
Los médicos independientes no necesitan un EHR (historia clínica electrónica) ni un CRM empresarial con pipelines de ventas. Necesitan algo tan simple como una lista priorizada de "a quién escribirle hoy" con el mensaje ya redactado. El 80% del valor está en ese momento de fricción cero.

**Funcionalidades del MVP:**
- Dashboard con 4 métricas de estado (sin contacto, cita próxima, inactivos, total)
- Generación de mensajes personalizados por IA (DeepSeek-V3) en español peruano
- Links de WhatsApp con mensaje prellenado — el médico solo toca "Enviar"
- Registro de pacientes por nota de voz (Whisper transcribe, IA extrae datos estructurados)
- Campañas de temporada (Navidad, Año Nuevo, control anual) para toda la base

---

## 5. Why Now?

- <a href="https://www.cmp.org.pe">Colegio Médico del Perú</a> registra 68,761 médicos habilitados (2024), con WhatsApp a +90% de penetración en Perú — el canal ya existe, falta la inteligencia
- DeepSeek-V3 reduce el costo de generar un mensaje personalizado a $0.001 — hace 3 años esto costaba 100x más
- Whisper large-v3 transcribe voz en español con precisión casi perfecta — registro de pacientes por audio sin esfuerzo
- El sector salud privada creció a tasa compuesta del 10% entre 2022-2024, alcanzando S/. 4,600M de facturación (TMS/Gestión, 2024) — los médicos independientes están ganando más y necesitan retener pacientes
- Claude Code permite construir y desplegar este producto en días, no meses — la barrera de ejecución desapareció

---

## 6. Mercado

| Nivel | Definición | Cálculo | Tamaño |
|---|---|---|---|
| **TAM** | Médicos independientes en Latinoamérica | ~800,000 médicos × $30/mes × 12 | **$288M/año** |
| **SAM** | Médicos independientes en Perú con gestión por WhatsApp | ~20,000 médicos × S/.79/mes × 12 | **S/.19M/año** |
| **SOM** | Lima Metropolitana, primeros 12 meses | 500 usuarios × S/.79/mes × 12 | **S/.474K/año** |

**Fuentes:**
- Colegio Médico del Perú: 68,761 médicos habilitados en Perú (2024)
- OPS: densidad médica en Latinoamérica (~2M médicos totales)
- TMS/Gestión: sector salud privada Lima facturación S/.4,600M en 2024, crecimiento anual >9%
- INEI: estadísticas de recursos humanos en salud 2015-2024

---

## 7. Competencia y Moat

| | SeguiMed | Excel / Libreta | WhatsApp solo | Doctoralia | HubSpot |
|---|---|---|---|---|---|
| Seguimiento automático | ✅ | ❌ | ❌ | Parcial | ✅ |
| Genera mensajes con IA | ✅ | ❌ | ❌ | ❌ | ❌ |
| Precio accesible | ✅ S/.49-199 | Gratis | Gratis | S/.300+ | S/.500+ |
| Diseñado para médico independiente LatAm | ✅ | ❌ | ❌ | ❌ | ❌ |
| Setup en menos de 5 minutos | ✅ | ❌ | ✅ | ❌ | ❌ |
| Registro por voz | ✅ | ❌ | ❌ | ❌ | ❌ |

**Moat:**
- Precio inaccesible para grandes players (S/.49/mes destruye el margen de Doctoralia)
- Simplicidad extrema diseñada para el médico no-técnico
- Contexto médico LatAm: mensajes entrenados en español peruano, campos adaptados a la realidad local
- Datos propios de patrones de comunicación médico-paciente que se acumulan con el tiempo
- Distribución boca a boca dentro de redes médicas cerradas (un médico refiere a 5 colegas)

---

## 8. Producto — Demo y Arquitectura

**Demo en vivo:** [https://seguimed.streamlit.app](https://seguimed.streamlit.app)  
**Credenciales de prueba:** contraseña `demo1234`

**Repositorio:** [https://github.com/MayraOA/seguimed](https://github.com/MayraOA/seguimed)

**Flujo principal del usuario:**
1. Médico ingresa a la app → login simple con contraseña
2. Dashboard muestra pacientes priorizados por días sin contacto
3. Clic en "Generar mensaje" → DeepSeek crea mensaje personalizado en español
4. Clic en "WhatsApp" → abre WhatsApp con mensaje prellenado, el médico solo envía
5. Registro de nuevo paciente: formulario manual o nota de voz (Whisper transcribe automáticamente)
6. Campañas: genera mensajes para toda la base en una campaña de temporada

**Diagrama de arquitectura:**

```
[Médico] → [Streamlit App]
               ├── [Supabase PostgreSQL] → patients, contacts
               ├── [DeepSeek-V3 API] → generación de mensajes
               ├── [Groq Whisper API] → transcripción de voz
               └── [WhatsApp deep links] → wa.me/{phone}?text={mensaje}

Deploy: Streamlit Community Cloud (gratuito)
CI/CD: GitHub Actions (flake8 lint)
```

**Herramientas de IA del curso utilizadas:**
- **DeepSeek-V3** (`utils/ai.py` → `generate_message()`): generación de mensajes personalizados en español peruano. Elegido por relación costo-rendimiento: $0.001/mensaje vs $0.01 de GPT-4o.
- **Whisper large-v3 via Groq** (`utils/ai.py` → `transcribe_audio()`): transcripción de notas de voz del médico para registro de pacientes. Mismo modelo visto en clase, latencia <2 segundos, tier gratuito.

**Estructura del repositorio:**
```
seguimed/
├── app.py                    # Entry point, login, sidebar
├── pages/
│   ├── 1_dashboard.py        # Métricas + tabla priorizada + generación de mensajes
│   ├── 2_patients.py         # Lista, búsqueda y detalle de pacientes
│   ├── 3_new_patient.py      # Alta manual + registro por voz (Whisper)
│   ├── 4_campaigns.py        # Campañas masivas de temporada
│   └── 5_settings.py         # Configuración del médico
├── utils/
│   ├── ai.py                 # DeepSeek + Groq Whisper
│   ├── database.py           # CRUD Supabase + fallback demo
│   └── whatsapp.py           # Generador de links wa.me
├── docs/                     # Pitch, screenshots, investigación, branding
├── .streamlit/config.toml    # Tema visual SeguiMed
├── .github/workflows/ci.yml  # CI: flake8 lint ✅
└── requirements.txt
```

---

## 9. Modelo de Negocio y Pricing

**Modelo:** SaaS mensual por suscripción

| Plan | Precio | Límite | Para quién |
|---|---|---|---|
| **Básico** | S/.49/mes | 100 pacientes | Médico que empieza |
| **Pro** | S/.99/mes | 500 pacientes + campañas + recordatorios | Médico establecido |
| **Clínica** | S/.199/mes | Ilimitado + múltiples usuarios | Consultorio pequeño |

**Unit economics:**

| Concepto | Valor |
|---|---|
| ARPU (Plan Pro) | S/.99/mes |
| Costo variable por usuario/mes | ~S/.0.50 (DeepSeek + hosting) |
| Contribution margin | ~99% |
| Payback period | Mes 1 |
| LTV estimado (12 meses, churn 5%/mes) | ~S/.780 |

---

## 10. Go-to-Market (GTM)

**Primeros 10 usuarios — red directa:**
- Médico familiar del founder (beta piloto activo)
- Colegas referidos por el médico piloto (mismo hospital/clínica)
- Estrategia: demo en persona, onboarding de 5 minutos

**Primeros 100 usuarios — comunidades médicas:**
- Grupos de WhatsApp de médicos independientes en Lima (existen decenas por especialidad)
- Eventos del Colegio Médico del Perú (CMP) — Lima y provincias
- Facebook: grupos "Médicos del Perú", "Médicos Independientes Lima"

**Primeros 1,000 usuarios — escalamiento:**
- Alianzas con distribuidores de equipos médicos (acceso a red de médicos compradores)
- Especialidades de alta rotación de pacientes: nutricionistas, psicólogos, dermatólogos
- Expansión geográfica: Arequipa, Trujillo (segundo y tercer mercado)
- Expansión internacional: Colombia (mismo idioma, mismo problema)

---

## 11. Tracción / Señales Tempranas

- **Demo desplegado y funcionando:** [https://seguimed.streamlit.app](https://seguimed.streamlit.app)
- **Usuario beta piloto:** médico independiente en Lima (validación de flujo completo)
- **5 entrevistas de validación** con médicos independientes — ver `docs/research/`
- **Dolor confirmado en entrevistas:** *(completar con hallazgos reales)*
- **Disposición a pagar confirmada:** *(completar con rangos mencionados en entrevistas)*

---

## 12. Roadmap

| Plazo | Hito |
|---|---|
| **3 meses** | 50 usuarios pagos en Lima · integración WhatsApp Business API |
| **6 meses** | 200 usuarios · app móvil (React Native) · módulo de agenda de citas |
| **12 meses** | 500 usuarios · expansión Colombia y Chile · modelo fine-tuneado en conversaciones médico-paciente LatAm |

---

## 13. Riesgos y Mitigación

| Riesgo | Severidad | Mitigación |
|---|---|---|
| **Regulatorio:** datos sensibles de pacientes (Ley 29733, Perú) | Media | No almacenamos historial clínico, solo metadata de contacto. Términos de uso claros. Asesoría legal antes de escalar. |
| **Adopción:** médicos mayores con baja cultura digital | Media | Onboarding de 5 minutos, soporte por WhatsApp del propio founder, demo con el teléfono del médico. |
| **Competencia:** Doctoralia o HubSpot añaden esta función | Baja | Moat en precio (S/.49/mes), simplicidad y contexto LatAm. Grandes players no pueden bajar a ese precio sin destruir margen. |

---

## 14. The Ask

> **"Buscamos S/.50,000 (~$13,500 USD) para 6 meses de runway."**

**Uso del capital:**
- S/.20,000 → Marketing directo a médicos independientes en Lima
- S/.15,000 → Desarrollo de integración WhatsApp Business API
- S/.15,000 → Operaciones, soporte y legal básico

**Milestone que desbloquea ese capital:**  
200 usuarios pagos con churn mensual menor al 5% — punto de validación de product-market fit.

**¿Por qué invertir ahora?**  
El producto funciona, el mercado está validado, la ventana tecnológica está abierta y la fundadora está ejecutando.
