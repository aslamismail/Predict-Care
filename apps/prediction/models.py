from django.db import models
from django.conf import settings

class DiseasePrediction(models.Model):
    DISEASE_CHOICES = [
        ('lung_cancer', 'Lung Cancer'),
        ('heart_disease', 'Heart Disease'),
        ('diabetes', 'Diabetes'),
        ('parkinsons', "Parkinson's"),
        ('arthritis', 'Arthritis'),
        ('asthma', 'Asthma'),
        ('liver_disease', 'Liver Disease')
    ]
    
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disease_type = models.CharField(max_length=20, choices=DISEASE_CHOICES)
    
    prediction_result = models.CharField(max_length=50)
    confidence_score = models.FloatField()
    risk_factors = models.TextField()
    severity_level = models.CharField(max_length=20)
    
    recommended_treatment = models.TextField(null=True, blank=True)
    follow_up_schedule = models.DateField(null=True, blank=True)
    preventive_measures = models.TextField(null=True, blank=True)
    
    predicted_at = models.DateTimeField(auto_now_add=True)

    patient_values = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.get_disease_type_display()} Prediction"
