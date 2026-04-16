from django.db import models

class FormResponse(models.Model):
    lead_id = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255)
    form_step = models.IntegerField()
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead_id} – Step {self.form_step}"
