from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MedicalHistory
from django.contrib import messages
from django.contrib.auth import logout
from apps.prediction.models import DiseasePrediction
from .forms import AppointmentForm
from apps.doctor.models import Appointment
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@login_required
def medical_history_form(request):
    if request.method == 'POST':
        # Check if patient already has a medical history
        medical_history, created = MedicalHistory.objects.get_or_create(patient=request.user)
        
        # Update medical history fields
        medical_history.blood_pressure = request.POST.get('blood_pressure')
        medical_history.cholesterol_level = request.POST.get('cholesterol_level')
        medical_history.heart_rate = request.POST.get('heart_rate')
        medical_history.smoking_status = request.POST.get('smoking_status')
        medical_history.alcohol_consumption = request.POST.get('alcohol_consumption')
        medical_history.physical_activity_level = request.POST.get('physical_activity_level')
        medical_history.blood_sugar = request.POST.get('blood_sugar')
        medical_history.hba1c_level = request.POST.get('hba1c_level')
        medical_history.systolic_bp = request.POST.get('systolic_bp')
        medical_history.diastolic_bp = request.POST.get('diastolic_bp')
        medical_history.cholesterol_ldl = request.POST.get('cholesterol_ldl')
        medical_history.cholesterol_hdl = request.POST.get('cholesterol_hdl')
        medical_history.cholesterol_triglycerides = request.POST.get('cholesterol_triglycerides')
        
        # Family history
        medical_history.family_history_diabetes = request.POST.get('family_history_diabetes') == 'on'
        medical_history.family_history_heart_disease = request.POST.get('family_history_heart_disease') == 'on'
        medical_history.family_history_lungcancer = request.POST.get('family_history_lungcancer') == 'on'
        medical_history.family_history_asthma = request.POST.get('family_history_asthma') == 'on'
        medical_history.family_history_liver_disease = request.POST.get('family_history_liver_disease') == 'on'
        medical_history.family_history_parkinsons = request.POST.get('family_history_parkinsons') == 'on'
        
        # Additional details
        medical_history.existing_conditions = request.POST.get('existing_conditions')
        medical_history.current_medications = request.POST.get('current_medications')
        
        medical_history.save()
        
        messages.success(request, 'Medical history updated successfully!')
        return redirect('patient:dashboard')
    
    return render(request, 'patient/medical_history.html')

@login_required
def patient_dashboard(request):
    try:
        medical_history = MedicalHistory.objects.get(patient=request.user)
    except MedicalHistory.DoesNotExist:
        medical_history = None
    
    recent_predictions = DiseasePrediction.objects.filter(patient=request.user).order_by('-predicted_at')[:1]
    first_prediction = recent_predictions.first()

    return render(request, 'patient/dashboard.html', {
        'medical_history': medical_history,
        'recent_predictions': first_prediction,
    })

def custom_logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def view_medical_history(request):
    medical_history = MedicalHistory.objects.filter(patient=request.user).first()
    return render(request, 'patient/view_medical_history.html', {'medical_history': medical_history})

@login_required
def book_appointment(request):
    referrer = request.GET.get('referrer', '').strip('/')
    base_url = request.build_absolute_uri('/').rstrip('/')
    predictiourl= f"{base_url}/{referrer}" if referrer else ""

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.patient_name = request.user.name
            appointment.save()
            messages.success(request, 'Appointment Scheduled Successfully!')
            return redirect('patient:dashboard')
        else:
            messages.warning(request, 'An error occured. Please fill all the fields and try again.')

    else:
        form = AppointmentForm()
    
    return render(request, 'patient/book_appointment.html', {'form': form, 'referrer': predictiourl})

def view_doc_profile(request, doctor_id):
    User = get_user_model()
    doctor = get_object_or_404(User, id=doctor_id)
    return render(request, "patient/doctor_profile.html", {"doctor": doctor})

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date')
    return render(request, "patient/my_appointments.html", {"appointments": appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if appointment.status == "scheduled":
        appointment.status = "cancelled"
        appointment.save()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "message": "Cannot cancel this appointment."}, status=400)