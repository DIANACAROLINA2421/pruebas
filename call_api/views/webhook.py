from rest_framework.decorators import api_view
from rest_framework.response import Response
from call_api.models.lead_resume import LeadResume


@api_view(['POST'])
def lobees_webhook(request):

    data = request.data
    print("Datos recibidos de Lobees:", data)
    return Response({"status": "ok"})


@api_view(['POST'])
def register_resume_info(request):


    lead_id = request.data.get("lead_id")
    task_id = request.data.get("task_id")
    execution_id = request.data.get("execution_id")

    if not lead_id or not task_id or not execution_id:
        return Response(
            {"error": "lead_id, task_id y execution_id son requeridos"},
            status=400
        )

    LeadResume.objects.update_or_create(
        lead_id=lead_id,
        task_id=task_id,
        defaults={"execution_id": execution_id}
    )

    print(f"--- REGISTRO LOBEES --- Lead: {lead_id} | Task: {task_id} | Execution: {execution_id}")

    return Response({
        "status": "registered",
        "lead_id": lead_id,
        "task_id": task_id,
        "execution_id": execution_id
    })
