from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    user_type = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'email', 'user_type', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'profile_picture')

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age', 'gender', 'height', 'weight', 'bmi', 'address', 'city', 'state', 'zip_code', 'phone_number', 'country']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['medical_license_number', 'specialization', 'degree', 'hospital', 'experience', 'about', 'phone_number', 'registration', 'languages','office_hours']
