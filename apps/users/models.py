from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin')
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    SPECIALIZATION_CHOICES = (
        ("General Physician", "General Physician"),
        ("Cardiologist", "Cardiologist"),  # Heart disease
        ("Endocrinologist", "Endocrinologist"),  # Diabetes
        ("Pulmonologist", "Pulmonologist"),  # Asthma, lung diseases
        ("Neurologist", "Neurologist"),  # Parkinson’s
        ("Hepatologist", "Hepatologist"),  # Liver disease
        ("Oncologist", "Oncologist"),  # Lung cancer, other cancers
        ("Nephrologist", "Nephrologist"),  # Kidney diseases
        ("Gastroenterologist", "Gastroenterologist"),  # Digestive system, liver disease
        ("Rheumatologist", "Rheumatologist"),  # Autoimmune diseases
        ("Allergist/Immunologist", "Allergist/Immunologist"),  # Asthma, allergies
        ("Pulmonary Critical Care", "Pulmonary Critical Care"),  # Severe lung conditions
        ("Geriatrician", "Geriatrician"),  # Elderly care, chronic diseases
        ("Endoscopic Surgeon", "Endoscopic Surgeon"),  # Liver & digestive tract surgeries
        ("Internal Medicine", "Internal Medicine"),
        ("Psychiatrist", "Psychiatrist"),  # Neurological & psychological disorders
        ("Pediatrician", "Pediatrician"),  # Child diseases including asthma
        ("Thoracic Surgeon", "Thoracic Surgeon"),  # Lung & chest surgeries
        ("Vascular Surgeon", "Vascular Surgeon"),  # Circulatory diseases
        ("Dermatologist", "Dermatologist"),  # Skin diseases
        ("ENT Specialist", "ENT Specialist"),  # Ear, nose, throat issues
        ("Radiologist", "Radiologist"),  # Imaging for lung cancer, heart disease
        ("Anesthesiologist", "Anesthesiologist"),  # Surgery support
        ("Sports Medicine Specialist", "Sports Medicine Specialist"),  # Physical injuries
        ("Community Medicine Specialist", "Community Medicine Specialist"),  # Public health
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    name = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Patient-specific fields
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER_CHOICES)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
                               
    # Doctor-specific fields
    medical_license_number = models.CharField(max_length=50, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True, choices=SPECIALIZATION_CHOICES)
    degree = models.CharField(help_text="Enter multiple degrees separated by commas (e.g., MBBS, MD, DM)", max_length=50, null=True, blank=True)
    hospital= models.CharField(max_length=50, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    registration = models.TextField(null=True, blank=True)
    languages = models.CharField(max_length=100, null=True, blank=True)
    office_hours = models.CharField(max_length=100, null=True, blank=True)

    def is_patient(self):
        return self.user_type == 'patient'

    def is_doctor(self):
        return self.user_type == 'doctor'
