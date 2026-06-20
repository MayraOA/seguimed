import os
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

_supabase = None
DEMO_MODE = False


def get_client():
    global _supabase, DEMO_MODE
    if _supabase is not None:
        return _supabase
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Missing Supabase credentials")
        _supabase = create_client(url, key)
        return _supabase
    except Exception:
        DEMO_MODE = True
        return None


def _demo_patients():
    today = datetime.now().date()
    return [
        {
            "id": "1", "name": "Juan Pérez", "phone": "+51987654321",
            "last_contact_date": str(today - timedelta(days=10)),
            "next_appointment": None, "diagnosis": "Dolor de rodilla",
            "notes": "Paciente con inflamación crónica", "status": "active",
            "created_at": str(today - timedelta(days=30)),
        },
        {
            "id": "2", "name": "María García", "phone": "+51976543210",
            "last_contact_date": str(today - timedelta(days=2)),
            "next_appointment": str(today + timedelta(days=1)),
            "diagnosis": "Diabetes tipo 2", "notes": "Control mensual de glucosa",
            "status": "active", "created_at": str(today - timedelta(days=60)),
        },
        {
            "id": "3", "name": "Carlos López", "phone": "+51965432109",
            "last_contact_date": str(today - timedelta(days=25)),
            "next_appointment": None, "diagnosis": "Post-operatorio de hernia",
            "notes": "Revisión de cicatriz pendiente", "status": "active",
            "created_at": str(today - timedelta(days=40)),
        },
        {
            "id": "4", "name": "Ana Torres", "phone": "+51954321098",
            "last_contact_date": str(today - timedelta(days=45)),
            "next_appointment": None, "diagnosis": "Control rutinario",
            "notes": "Exámenes de laboratorio pendientes", "status": "active",
            "created_at": str(today - timedelta(days=90)),
        },
        {
            "id": "5", "name": "Luis Mendoza", "phone": "+51943210987",
            "last_contact_date": str(today - timedelta(days=1)),
            "next_appointment": str(today + timedelta(days=5)),
            "diagnosis": "Hipertensión arterial", "notes": "Medicación controlada",
            "status": "active", "created_at": str(today - timedelta(days=20)),
        },
    ]


def get_all_patients():
    client = get_client()
    if DEMO_MODE or client is None:
        return _demo_patients()
    try:
        res = client.table("patients").select("*").order("last_contact_date", desc=False).execute()
        return res.data or []
    except Exception:
        return _demo_patients()


def get_patient(patient_id):
    client = get_client()
    if DEMO_MODE or client is None:
        return next((p for p in _demo_patients() if p["id"] == str(patient_id)), None)
    try:
        res = client.table("patients").select("*").eq("id", patient_id).single().execute()
        return res.data
    except Exception:
        return None


def insert_patient(data: dict):
    client = get_client()
    if DEMO_MODE or client is None:
        return {"success": False, "error": "Modo demo: no se puede guardar"}
    try:
        res = client.table("patients").insert(data).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_patient(patient_id, data: dict):
    client = get_client()
    if DEMO_MODE or client is None:
        return {"success": False, "error": "Modo demo: no se puede actualizar"}
    try:
        res = client.table("patients").update(data).eq("id", patient_id).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def log_contact(patient_id, message_sent, contact_type="whatsapp"):
    client = get_client()
    if DEMO_MODE or client is None:
        return {"success": False, "error": "Modo demo"}
    try:
        res = client.table("contacts").insert({
            "patient_id": patient_id,
            "message_sent": message_sent,
            "contact_type": contact_type,
        }).execute()
        client.table("patients").update(
            {"last_contact_date": datetime.now().date().isoformat()}
        ).eq("id", patient_id).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_contacts_for_patient(patient_id):
    client = get_client()
    if DEMO_MODE or client is None:
        return []
    try:
        res = (
            client.table("contacts")
            .select("*")
            .eq("patient_id", patient_id)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data or []
    except Exception:
        return []


def search_patients(query: str):
    all_p = get_all_patients()
    q = query.lower()
    return [
        p for p in all_p
        if q in p.get("name", "").lower() or q in p.get("phone", "").lower()
    ]


def get_dashboard_stats():
    patients = get_all_patients()
    today = datetime.now().date()
    week_later = today + timedelta(days=7)

    no_contact_7 = []
    appt_this_week = []
    inactive_30 = []
    actives = []

    for p in patients:
        if p.get("status") != "active":
            continue
        actives.append(p)

        lc = p.get("last_contact_date")
        last_dt = datetime.strptime(lc, "%Y-%m-%d").date() if lc else None
        days_since = (today - last_dt).days if last_dt else 999

        p["_days_since"] = days_since

        if days_since >= 7:
            no_contact_7.append(p)
        if days_since >= 30:
            inactive_30.append(p)

        na = p.get("next_appointment")
        if na:
            na_dt = datetime.strptime(na, "%Y-%m-%d").date()
            if today <= na_dt <= week_later:
                appt_this_week.append(p)

    prioritized = sorted(actives, key=lambda x: x.get("_days_since", 0), reverse=True)

    return {
        "no_contact_7": len(no_contact_7),
        "appt_this_week": len(appt_this_week),
        "inactive_30": len(inactive_30),
        "total_active": len(actives),
        "prioritized": prioritized,
    }
