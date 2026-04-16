from django.contrib import admin
from call_api.models.form_response import FormResponse
from call_api.models.lead_resume import LeadResume

@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    list_display = ("lead_id", "task_id", "form_step", "created_at")
    search_fields = ("lead_id", "task_id")
    list_filter = ("form_step",)

@admin.register(LeadResume)
class LeadResumeAdmin(admin.ModelAdmin):
    list_display = ("lead_id", "task_id", "execution_id")
    search_fields = ("lead_id", "task_id")
