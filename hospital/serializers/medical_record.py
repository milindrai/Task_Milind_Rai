from rest_framework import serializers
from hospital.models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'symptoms', 'diagnosis', 'treatment', 'created_at']
        read_only_fields = ['id', 'created_at'] 