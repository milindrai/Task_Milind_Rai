from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('patients/', views.PatientListCreateView.as_view(), name='patients'),
    path('patients/records/add', views.MedicalRecordCreateView.as_view(), name='add_record'),
    path('patients/<int:pk>/records/', views.PatientMedicalRecordsView.as_view(), name='patient_records'),
] 