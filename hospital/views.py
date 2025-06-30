from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from hospital.models import Patient, MedicalRecord, UserProfile
from hospital.serializers.user import UserSignupSerializer
from hospital.serializers.patient import PatientSerializer
from hospital.serializers.medical_record import MedicalRecordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Patient.objects.all()
        return Patient.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MedicalRecordCreateView(generics.CreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({'detail': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not (request.user.is_superuser or patient.created_by == request.user):
            raise PermissionDenied('You do not have permission to add records to this patient.')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PatientMedicalRecordsView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['pk']
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise PermissionDenied('Patient not found.')
        user = self.request.user
        if not (user.is_superuser or patient.created_by == user):
            raise PermissionDenied('You do not have permission to view records for this patient.')
        return MedicalRecord.objects.filter(patient=patient)
