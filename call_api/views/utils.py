import requests
from call_api.models.lead_resume import LeadResume

LOBEES_API_URL = "https://api.lobees.com/api/project/addtasklog"
LOBEES_TOKEN = "your-lobees-token-here"  # ← reemplaza con tu token real


def send_to_lobees(lead_id, task_id, step, data):
    resume_info = LeadResume.objects.filter(
        lead_id=lead_id,
        task_id=task_id
    ).first()

    if not resume_info:
        return 500, {"error": "No existe LeadResume para este lead + task"}

    url = f"http://localhost:5678/webhook-waiting/form{step}_{lead_id}"

    payload = {
        "lead_id": lead_id,
        "task_id": task_id,
        "step": step,
        "data": data
    }

    response = requests.post(url, json=payload)
    try:
        return response.status_code, response.json()
    except:
        return response.status_code, {"message": response.text}


def add_task_log(task_id, description, percent=0):

    payload = {
        "projecttask": task_id,
        "hours": 0,
        "description": description,
        "taskpercent": percent
    }

    headers = {
        "Authorization": f"Bearer {LOBEES_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(LOBEES_API_URL, json=payload, headers=headers, timeout=5)
        print(f"Log Lobees [{percent}%]: {description} → {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error registrando log en Lobees: {e}")
        return 500