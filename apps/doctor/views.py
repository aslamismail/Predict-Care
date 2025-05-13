from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, Treatment, TreatmentNote, PrescribedMedication
from django.urls import reverse
from django.views.decorators.http import require_POST
from apps.prediction.models import DiseasePrediction
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages

User = get_user_model()

"""
@login_required
def patient_list(request):
    # Only doctors can access this view
    if not request.user.is_doctor():
        return render(request, '403.html')
    
    # Get all patients with their disease predictions
    patients = User.objects.filter(user_type='patient')
    patient_data = []
    
    for patient in patients:
        predictions = DiseasePrediction.objects.filter(patient=patient).order_by('-predicted_at')[:5]
        patient_data.append({
            'patient': patient,
            'predictions': predictions
        })
    
    return render(request, 'doctor/patient_list.html', {
        'patient_data': patient_data
    })

@login_required
def patient_detail(request, patient_id):
    # Only doctors can access this view
    if not request.user.is_doctor():
        return render(request, '403.html')
    
    patient = get_object_or_404(User, id=patient_id)
    medical_history = patient.medicalhistory
    disease_predictions = DiseasePrediction.objects.filter(patient=patient)
    
    return render(request, 'doctor/patient_detail.html', {
        'patient': patient,
        'medical_history': medical_history,
        'disease_predictions': disease_predictions
    })
"""
def get_doctors_by_specialization(request):
    specialization = request.GET.get('specialization', None)
    if specialization:
        doctors = User.objects.filter(user_type="doctor", specialization=specialization).values('id', 'username', 'name', 'hospital')
        return JsonResponse(list(doctors), safe=False)
    return JsonResponse([], safe=False)

@login_required
def doctor_appointments(request):
    # Fetch only the appointments of the logged-in doctor
    appointments = Appointment.objects.filter(doctor=request.user).order_by('-date')

    return render(request, "doctor/appointments.html", {"appointments": appointments})

@login_required
def update_appointment_status(request, appointment_id, new_status):
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=request.user)
        if new_status in ["completed", "cancelled"]:
            appointment.status = new_status
            appointment.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "Invalid status!"})
    except Appointment.DoesNotExist:
        return JsonResponse({"success": False, "message": "Appointment not found!"})
    
@login_required
def get_doctor_appointments(request):
    appointments = Appointment.objects.all()
    events = [
        {
            "id": appt.id,
            "title": f"Appointment with {appt.patient.username}",
            "start": appt.date.isoformat(),
            "backgroundColor": "#007bff" if appt.status == "scheduled" else 
                               "#28a745" if appt.status == "completed" else "#dc3545",
            "extendedProps": {
                "status": appt.status,  # Ensure status is properly set
                "patient": appt.patient.username,
                "reason": appt.reason,
            },
        }
        for appt in appointments
    ]
    return JsonResponse(events, safe=False)

def delete_appointment(request, appointment_id):
    if request.method == "DELETE":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def create_treatment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Ensure the appointment is completed before creating treatment
    if appointment.status != "completed":
        return JsonResponse({"success": False, "message": "Appointment must be completed first."}, status=400)
    
    # Check if a treatment already exists
    if Treatment.objects.filter(patient=appointment.patient, doctor=appointment.doctor).exists():
        return JsonResponse({"success": False, "message": "Treatment record already exists."}, status=400)

    # Create the treatment record
    Treatment.objects.create(
        doctor=appointment.doctor,
        patient=appointment.patient
    )

    return JsonResponse({"success": True, "message": "Treatment created successfully."})

@login_required
def patient_list(request):
    doctor = request.user  # Get the logged-in doctor
    patients = (
        Treatment.objects.filter(doctor=doctor)
        .select_related("patient")
        .values("patient__id", "patient__username", "patient__email", "patient__name", "patient__phone_number", "patient__profile_picture", "patient__age", "patient__gender")
        .distinct()
    )

    return render(request, "doctor/patient_list.html", {"patients": patients})

@login_required
def patient_treatment(request, patient_id):
    doctor = request.user
    # treatment = Treatment.objects.filter(doctor=doctor, patient_id=patient_id).select_related("patient")
    predictions = DiseasePrediction.objects.filter(patient_id=patient_id).order_by('-predicted_at')[:5]
    treatment = get_object_or_404(Treatment, doctor=doctor, patient_id=patient_id)
    notes = treatment.notes.all()  # Get all notes for this treatment
    medications = treatment.medications.all()  # Get all prescribed medications

    # if not treatment.exists():
    #    return render(request, "doctor/no_treatments.html", {"patient_id": patient_id})

    return render(request, "doctor/treatment_detail.html", {
        "treatment": treatment, 
        "patient": treatment.patient,
        "notes": notes,
        "medications": medications,
        "predictions": predictions,
    })

def add_note(request, treatment_id):
    if request.method == 'POST':
        treatment = get_object_or_404(Treatment, id=treatment_id)
        note_text = request.POST.get('note')
        if note_text:
            TreatmentNote.objects.create(treatment=treatment, note=note_text)
            messages.success(request, 'Note added successfully!')
            patient=treatment.patient.id
            base=f"/doctor/patient/{patient}/treatments/"
           # print("/patient/"+str(patient)+"/treatments/")
    return redirect(base)

def delete_note(request, note_id):
    note = get_object_or_404(TreatmentNote, id=note_id)
    treatment_id = note.treatment.id
    patient_id = note.treatment.patient.id

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
    
    # Redirect back to the treatment notes page
    return redirect(f'/doctor/patient/{patient_id}/treatments/')

# View to add a new prescription
@require_POST
def add_prescription(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    name = request.POST.get('name')
    dosage = request.POST.get('dosage')
    instructions = request.POST.get('instructions')
    
    if name and dosage and instructions:
        PrescribedMedication.objects.create(
            treatment=treatment,
            name=name,
            dosage=dosage,
            instructions=instructions,
        )
        patient=treatment.patient.id
        base=f"/doctor/patient/{patient}/treatments/"
    return redirect(base)


# View to delete a prescription
@require_POST
def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(PrescribedMedication, id=prescription_id)
    treatment_id = prescription.treatment.id
    prescription.delete()
    patient_id = prescription.treatment.patient.id
    return redirect(f'/doctor/patient/{patient_id}/treatments/')
"""
@login_required
def treatment_detail(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    notes = treatment.notes.all()  # Get all notes for this treatment
    medications = treatment.medications.all()  # Get all prescribed medications

    return render(request, "doctor/treatment_detail.html", {
        "treatment": treatment,
        "notes": notes,
        "medications": medications
    })
"""