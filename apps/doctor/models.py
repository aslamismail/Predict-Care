from django.db import models
from django.conf import settings

class Appointment(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    
    patient_name = models.CharField(max_length=50, default='')
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='scheduled')
    
    notes = models.TextField(null=True, blank=True)
    prediction_result = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Appointment for {self.patient.username} with Dr. {self.doctor.username}"
    

class Treatment(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_treatments")
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_treatments")

    diagnosis = models.TextField()
    follow_up_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Treatment for {self.patient.username} by Dr. {self.doctor.username}"

class TreatmentNote(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    def __str__(self):
        return f"Note on {self.created_at.strftime('%Y-%m-%d %H:%M')} for {self.treatment.patient.username}"
    
class PrescribedMedication(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name="medications")
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField()
    prescribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.dosage}) for {self.treatment.patient.username}"