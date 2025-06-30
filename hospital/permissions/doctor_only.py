from rest_framework.permissions import BasePermission
from hospital.models import Patient

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if isinstance(obj, Patient):
            return obj.created_by == request.user
        if hasattr(obj, 'patient'):
            return obj.patient.created_by == request.user
        return False 