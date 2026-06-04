import threading
import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from call_api.models.form_response import FormResponse
from call_api.services.lobees_service import send_to_lobees
from call_api.views.utils import add_task_log


def get_form_step3(request, lead_id, task_id):
    n8n_url = request.GET.get("n8n_url", "")
    return render(request, "step3.html", {
        "lead_id": lead_id,
        "task_id": task_id,
        "n8n_url": n8n_url
    })


def _background_step3(lead_id, task_id, data, n8n_url):
    try:
        add_task_log(task_id, "Formulario completo enviado por el lead", percent=100)
    except Exception as e:
        print(f"Error add_task_log paso 3: {e}")
    try:
        send_to_lobees(lead_id, task_id, 3, data)
    except Exception as e:
        print(f"Error send_to_lobees paso 3: {e}")
    if n8n_url:
        n8n_url_real = n8n_url.replace("http://localhost:5678", "https://n8n.mpforall.com")
        try:
            requests.post(n8n_url_real, json={"completed": True}, timeout=10)
            print(f"n8n notificado paso 3: {n8n_url_real}")
        except Exception as e:
            print(f"Error n8n paso 3: {e}")


@api_view(['POST'])
def submit_step3(request):
    lead_id = request.data.get("lead_id")
    task_id = request.data.get("task_id")
    data = request.data.get("response")
    n8n_url = request.data.get("n8n_url")

    if not lead_id or not task_id:
        return Response({"error": "lead_id y task_id son requeridos"}, status=400)

    FormResponse.objects.create(
        lead_id=lead_id,
        task_id=task_id,
        form_step=3,
        data=data or {}
    )

    threading.Thread(
        target=_background_step3,
        args=(lead_id, task_id, data, n8n_url),
        daemon=True
    ).start()

    return Response({"status": "ok"}, status=201)