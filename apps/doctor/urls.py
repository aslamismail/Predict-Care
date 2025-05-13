from django.urls import path
from . import views
from .views import get_doctors_by_specialization
from .views import doctor_appointments
from .views import update_appointment_status, add_note, delete_note, add_prescription, delete_prescription, get_doctor_appointments, delete_appointment, create_treatment, patient_treatment#, treatment_detail

app_name = 'doctor'

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
   # path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('get-doctors/', get_doctors_by_specialization, name='get_doctors'),
    path("appointments/", doctor_appointments, name="appointments"),
    path("update-appointment/<int:appointment_id>/<str:new_status>/", update_appointment_status, name="update_appointment"),
    path("get-appointments/", get_doctor_appointments, name="get_doctor_appointments"),
    path("delete-appointment/<int:appointment_id>/", delete_appointment, name="delete-appointment"),
    path("create-treatment/<int:appointment_id>/", create_treatment, name="create-treatment"),
    path("patient/<int:patient_id>/treatments/", patient_treatment, name="patient-treatment"),
    path('treatment/<int:treatment_id>/add_note/', add_note, name='add_note'),
    path('note/<int:note_id>/delete/', delete_note, name='delete_note'),
    #path('treatment/<int:treatment_id>/', views.treatment_detail, name='treatment_detail'),
    path('treatment/<int:treatment_id>/add_prescription/', add_prescription, name='add_prescription'),
    path('prescription/<int:prescription_id>/delete/', delete_prescription, name='delete_prescription'),
    # path("treatment/<int:treatment_id>/", treatment_detail, name="treatment-detail"),
]
