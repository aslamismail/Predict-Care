from django import forms
from apps.doctor.models import Appointment
from apps.users.models import CustomUser

class AppointmentForm(forms.ModelForm):
    specialization = forms.ChoiceField(choices=CustomUser.SPECIALIZATION_CHOICES, required=True)
    
    class Meta:
        model = Appointment
        fields = ['specialization', 'doctor', 'date', 'reason', 'prediction_result']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = CustomUser.objects.filter(user_type="doctor")