import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from call_api.models.form_response import FormResponse
from call_api.services.lobees_service import send_to_lobees
from call_api.views.utils import add_task_log


def get_form_step1(request, lead_id, task_id):
    n8n_url = request.GET.get("n8n_url", "")
    return render(request, "step1.html", {
        "lead_id": lead_id,
        "task_id": task_id,
        "n8n_url": n8n_url
    })


@api_view(['POST'])
def submit_step1(request):
    lead_id = request.data.get("lead_id")
    task_id = request.data.get("task_id")
    data = request.data.get("response")
    n8n_url = request.data.get("n8n_url")

    if not lead_id or not task_id:
        return Response({"error": "lead_id y task_id son requeridos"}, status=400)

    FormResponse.objects.create(
        lead_id=lead_id,
        task_id=task_id,
        form_step=1,
        data=data or {}
    )

    send_to_lobees(lead_id, task_id, 1, data)
    add_task_log(task_id, "Formulario paso 1 enviado por el lead", percent=33)

    if n8n_url:
        n8n_url_real = n8n_url.replace("http://localhost:5678", "https://n8n.mpforall.com")
        try:
            requests.post(n8n_url_real, json={"completed": True}, timeout=5)
            print(f"n8n notificado exitosamente en paso 1 a {n8n_url_real}")
        except Exception as e:
            print(f"Error llamando a n8n en paso 1: {e}")

    return Response({"status": "ok"}, status=201)