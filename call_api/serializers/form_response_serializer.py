from rest_framework import serializers
from call_api.models.form_response import FormResponse

class FormResponseSerializer(serializers.ModelSerializer):

    def validate_form_step(self, value):
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("form_step inválido.")
        return value

    class Meta:
        model = FormResponse
        fields = [
            'id',
            'lead_id',
            'form_step',
            'data',
            'created_at'
        ]
