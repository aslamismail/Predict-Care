from django.db import models
from django.conf import settings

class MedicalHistory(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Personal Health Indicators
    blood_pressure = models.FloatField(max_length=20, null=True, blank=True)
    cholesterol_level = models.FloatField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    blood_sugar = models.FloatField(null=True, blank=True)
    hba1c_level = models.FloatField(null=True, blank=True)
    systolic_bp = models.FloatField(null=True, blank=True)
    diastolic_bp = models.FloatField(null=True, blank=True)
    cholesterol_ldl = models.FloatField(null=True, blank=True)
    cholesterol_hdl = models.FloatField(null=True, blank=True)
    cholesterol_triglycerides = models.FloatField(null=True, blank=True)
    
    # Lifestyle Factors
    smoking_status = models.CharField(max_length=50, choices=[
        ('non_smoker', 'Non-Smoker'),
        ('current_smoker', 'Current Smoker'),
        ('ex_smoker', 'Ex-Smoker')
    ], null=True, blank=True)
    
    alcohol_consumption = models.CharField(max_length=50, choices=[
        ('none', 'None'),
        ('occasional', 'Occasional'),
        ('moderate', 'Moderate'),
        ('heavy', 'Heavy')
    ], null=True, blank=True)
    
    physical_activity_level = models.CharField(max_length=50, choices=[
        ('sedentary', 'Sedentary'),
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('high', 'High')
    ], null=True, blank=True)
    
    # Family History
    family_history_diabetes = models.BooleanField(default=False)
    family_history_heart_disease = models.BooleanField(default=False)
    family_history_lungcancer = models.BooleanField(default=False)
    family_history_asthma = models.BooleanField(default=False)
    family_history_liver_disease = models.BooleanField(default=False)
    family_history_parkinsons = models.BooleanField(default=False)
    
    # Additional Medical Details
    existing_conditions = models.TextField(null=True, blank=True)
    current_medications = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Medical History for {self.patient.username}"
