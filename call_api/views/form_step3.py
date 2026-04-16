import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from call_api.models.form_response import FormResponse
from call_api.views.utils import send_to_lobees, add_task_log


def get_form_step3(request, lead_id, task_id):
    n8n_url = request.GET.get("n8n_url", "")
    return render(request, "step3.html", {
        "lead_id": lead_id,
        "task_id": task_id,
        "n8n_url": n8n_url
    })


@api_view(['POST'])
def submit_step3(request):
    lead_id = request.data.get("lead_id")
    task_id = request.data.get("task_id")
    data = request.data.get("response")


    FormResponse.objects.create(lead_id=lead_id, task_id=task_id, form_step=3, data=data)
    add_task_log(task_id, "Formulario completo enviado por el lead", percent=100)


    send_to_lobees(lead_id, task_id, 3, data)

    return Response({"status": "ok"}, status=201)
