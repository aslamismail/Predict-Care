from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import custom_logout_view
from .views import book_appointment
from .views import view_doc_profile
from .views import my_appointments
from .views import cancel_appointment

app_name = 'patient'

urlpatterns = [
    path('medical-history/', views.medical_history_form, name='medical_history'),
    path('dashboard/', views.patient_dashboard, name='dashboard'),
    path('logout/', custom_logout_view, name='logout'),
    path('view_medical_history/', views.view_medical_history, name='view_medical_history'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path("doctor_profile/<int:doctor_id>/", view_doc_profile, name="doctor_profile"),
    path("my-appointments/", my_appointments, name="my-appointments"),
    path("cancel-appointment/<int:appointment_id>/", cancel_appointment, name="cancel-appointment"),

]
