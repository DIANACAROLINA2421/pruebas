from django.urls import path
from call_api.views import form_step1, form_step2, form_step3
from call_api.views.webhook import register_resume_info

urlpatterns = [
    # Formularios HTML
    path('form/step1/<str:lead_id>/<str:task_id>/', form_step1.get_form_step1),
    path('form/step2/<str:lead_id>/<str:task_id>/', form_step2.get_form_step2),
    path('form/step3/<str:lead_id>/<str:task_id>/', form_step3.get_form_step3),

    # API POST
    path('api/submit-step1/', form_step1.submit_step1),
    path('api/submit-step2/', form_step2.submit_step2),
    path('api/submit-step3/', form_step3.submit_step3),

    # Webhook n8n
    path('api/register-resume/', register_resume_info),
]
