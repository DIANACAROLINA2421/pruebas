import requests
from decouple import config
from call_api.models.lead_resume import LeadResume

def send_to_lobees(lead_id, task_id, step, data):



    resume_info = LeadResume.objects.filter(
        lead_id=lead_id,
        task_id=task_id
    ).first()

    if resume_info:

        url_base = config("LOBEES_URL", default="").split("/webhook-waiting/")[0]
        url = f"{url_base}/webhook-waiting/{resume_info.execution_id}/form{step}_{lead_id}"
        print(f"--- USANDO EXECUTION_ID DINÁMICO: {resume_info.execution_id} ---")

    else:
        print("--- ADVERTENCIA: No existe LeadResume, usando URL base del .env ---")
        url_base = config("LOBEES_URL", default="")
        url = f"{url_base.rstrip('/')}/form{step}_{lead_id}"

    payload = {
        "lead_id": lead_id,
        "task_id": task_id,
        "step": step,
        "data": data
    }

    headers = {
        "Content-Type": "application/json"
    }

    token = config("LOBEES_TOKEN", default="")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        print(f"--- ENVIANDO A LOBEES (POST) --- URL: {url}")
        response = requests.post(url, json=payload, headers=headers, timeout=15)

        try:
            resp_json = response.json()
        except ValueError:
            resp_json = {"message": response.text or "Success (Empty response)"}

        return response.status_code, resp_json

    except Exception as e:
        return 500, {"error": str(e)}
