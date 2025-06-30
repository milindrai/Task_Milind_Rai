from rest_framework import serializers
from hospital.models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'address', 'created_by']
        read_only_fields = ['id', 'created_by']

    def validate_age(self, value):
        if value <= 0:
            raise serializers.ValidationError('Age must be greater than 0')
        return value 