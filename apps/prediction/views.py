from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DiseasePrediction
from apps.patient.models import MedicalHistory
from .ml_models.random_forest import predict_disease
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from apps.patient.forms import AppointmentForm
from apps.users.models import CustomUser
from django.contrib import messages

@login_required
def disease_prediction_dashboard(request):
    prediction_options = {
        'asthma': 'Asthma',
        'lung_cancer': 'Lung Cancer',
        'heart_disease': 'Heart Disease',
        'diabetes': 'Diabetes',
        'parkinsons': "Parkinson's",
        'liver_disease': 'Liver Disease',
    }

    recent_predictions = DiseasePrediction.objects.filter(patient=request.user).order_by('-predicted_at')[:5]

    return render(request, 'prediction/disease_dashboard.html', {
        'prediction_options': prediction_options.items(),
        'recent_predictions': recent_predictions
    })

@login_required
def predict_disease_risk(request, disease_type):
    user = request.user

    if request.method == "POST":
        if user.is_doctor():
            selected_patient_id = request.POST.get('selected_patient')
            if not selected_patient_id:
                return JsonResponse({"error": "Please select a patient."}, status=400)
            else:
                user = CustomUser.objects.get(id=selected_patient_id)

    if request.method == "POST":
        heart_disease= int(request.POST.get("heart_disease", 0))
        hypertension= int(request.POST.get("hypertension", 0))
        heartdisease= int(request.POST.get("HeartDisease", 0))
        stroke= int(request.POST.get("Stroke", 0))
        physicalHealth= int(request.POST.get("PhysicalHealth", 0))
        mentalHealth= int(request.POST.get("MentalHealth", 0))
        diffWalking= int(request.POST.get("DiffWalking", 0))
        race= int(request.POST.get("Race", 0))
        diabetic= int(request.POST.get("Diabetic", 0))
        physicalActivity= int(request.POST.get("PhysicalActivity", 0))
        genHealth= int(request.POST.get("GenHealth", 0))
        sleepTime= int(request.POST.get("SleepTime", 0))
        yellow_fingers= int(request.POST.get("yellow_fingers", 1))
        anxiety= int(request.POST.get("anxiety", 1))
        peer_pressure= int(request.POST.get("peer_pressure", 1))
        chronic_disease= int(request.POST.get("chronic_disease", 1))
        fatigue= int(request.POST.get("fatigue", 1))
        allergy= int(request.POST.get("allergy", 1))
        wheezing= int(request.POST.get("wheezing", 1))
        coughing= int(request.POST.get("coughing", 1))
        shortness_of_breath= int(request.POST.get("shortness_of_breath", 1))
        swallowing_difficulty= int(request.POST.get("swallowing_difficulty", 1))
        chest_pain= int(request.POST.get("chest_pain", 1))
        chest_pain_type= int(request.POST.get("chest_pain_type", 1))
        resting_ecg= int(request.POST.get("resting_ecg", 0))
        exercise_angina= int(request.POST.get("exercise_angina", 0))
        oldpeak= float(request.POST.get("oldpeak", 0))
        ST_slope= int(request.POST.get("ST_slope", 0))
        PhysicalActivity2= int(request.POST.get("PhysicalActivity2", 0))
        DietQuality= int(request.POST.get("DietQuality", 0))
        SleepQuality= int(request.POST.get("SleepQuality", 0))
        TraumaticBrainInjury= int(request.POST.get("TraumaticBrainInjury", 0))
        Hypertension2= int(request.POST.get("Hypertension2", 0))
        Diabetes2= int(request.POST.get("Diabetes2", 0))
        Depression= int(request.POST.get("Depression", 0))
        Stroke2= int(request.POST.get("Stroke2", 0))
        UPDRS= float(request.POST.get("UPDRS", 0))
        MoCA= float(request.POST.get("MoCA", 0))
        FunctionalAssessment= int(request.POST.get("FunctionalAssessment", 0))
        Tremor= int(request.POST.get("Tremor", 0))
        Rigidity= int(request.POST.get("Rigidity", 0))
        Bradykinesia= int(request.POST.get("Bradykinesia", 0))
        PosturalInstability= int(request.POST.get("PosturalInstability", 0))
        SpeechProblems= int(request.POST.get("SpeechProblems", 0))
        SleepDisorders= int(request.POST.get("SleepDisorders", 0))
        Constipation= int(request.POST.get("Constipation", 0))
        PhysicalActivity3= int(request.POST.get("PhysicalActivity3", 0))
        Diabetes3= int(request.POST.get("Diabetes3", 0))
        Hypertension3= int(request.POST.get("Hypertension3", 0))
        LiverFunctionTest= float(request.POST.get("LiverFunctionTest", 0))

    gender_mapping = {
        "Male": 0,
        "Female": 1
    }

    gender_for_model = gender_mapping.get(user.gender, -1)

     # Get medical history or prompt the user to enter it
    medical_history = MedicalHistory.objects.filter(patient=user).first()
    if not medical_history:
        if request.user.is_doctor():
            messages.warning(request, "This patient has no medical history available.")
            return redirect('prediction:dashboard')
        else:
            return redirect('patient:medical_history')  # Redirect to the form if missing

    medical_history = user.medicalhistory

    # print(f"Predicting disease risk for {disease_type} for user: {user.username}")
    if disease_type == 'asthma':
        smoking_mapping = {
            "non_smoker": 0,
            "current_smoker": 1,
            "ex_smoker": 1
        }

        alcohol_mapping = {
            "occasional": 0,
            "moderate": 1,
            "heavy": 1
        }
    
        #print(f"Predicting disease risk for {disease_type} for user: {user.gender}")
        smoking_status_for_model = smoking_mapping.get(medical_history.smoking_status, 0)
        alcohol_consumption_for_model = alcohol_mapping.get(medical_history.alcohol_consumption, 0)

        input_data = {
            "HeartDisease": heartdisease,
            "BMI": user.bmi,
            "Smoking": smoking_status_for_model,
            "AlcoholDrinking":alcohol_consumption_for_model,
            "Stroke": stroke,
            "PhysicalHealth": physicalHealth,
            "MentalHealth": mentalHealth,
            "DiffWalking": diffWalking,
            "Gender": gender_for_model,
            "Age": user.age,
            "Race": race, 
            "Diabetic": diabetic,
            "PhysicalActivity": physicalActivity,
            "GenHealth": genHealth,
            "SleepTime": sleepTime,
        }

    
    elif disease_type == 'lung_cancer':
        smoking_mapping = {
            "non_smoker": 1,
            "current_smoker": 2,
            "ex_smoker": 2
        }

        alcohol_mapping = {
            "occasional": 1,
            "moderate": 2,
            "heavy": 2
        }

        smoking_status_for_model = smoking_mapping.get(medical_history.smoking_status, 1)
        alcohol_consumption_for_model = alcohol_mapping.get(medical_history.alcohol_consumption, 1)

        input_data = {
            "gender": gender_for_model,
            "age": user.age,
            "smoking": smoking_status_for_model,
            "yellow_fingers": yellow_fingers,
            "anxiety": anxiety,
            "peer_pressure": peer_pressure,
            "chronic_disease": chronic_disease,
            "fatigue": fatigue,
            "allergy": allergy,
            "wheezing": wheezing,
            "alcohol_consuming": alcohol_consumption_for_model,
            "coughing": coughing,
            "shortness_of_breath": shortness_of_breath,
            "swallowing_difficulty": swallowing_difficulty,
            "chest_pain": chest_pain
        }

    elif disease_type == 'heart_disease':
        input_data = {
            "age": user.age,
            "gender": gender_for_model,
            "chest pain type": chest_pain_type,
            "resting bp s": medical_history.blood_pressure,
            "cholesterol": medical_history.cholesterol_level,
            "fasting blood sugar": medical_history.blood_sugar,
            "resting ecg": resting_ecg,
            "max heart rate": medical_history.heart_rate,
            "exercise angina": exercise_angina,
            "oldpeak": oldpeak,
            "ST slope": ST_slope
        }
    
    elif disease_type == 'diabetes':
        smoking_mapping = {
            "non_smoker": 0,
            "current_smoker": 2,
            "ex_smoker": 1
        }

        smoking_status_for_model = smoking_mapping.get(medical_history.smoking_status, -1)
        
        input_data = {
            'age': user.age,
            'gender': gender_for_model,
            'heart_disease': heart_disease,
            'hypertension': hypertension,
            'smoking_history': smoking_status_for_model,
            'bmi': user.bmi,
            'HbA1c_level': medical_history.hba1c_level,
            'blood_glucose_level': medical_history.blood_sugar,
        }
    
    elif disease_type == 'parkinsons':
        smoking_mapping = {
            "non_smoker": 0,
            "current_smoker": 1,
            "ex_smoker": 1
        }

        alcohol_mapping = {
            "occasional": 5,
            "moderate": 10,
            "heavy": 15
        }
    
        parkinsons_mapping = {
            False: 0,
            True: 1
        }

        #print(f"Predicting disease risk for {disease_type} for user: {user.gender}")
        smoking_status_for_model = smoking_mapping.get(medical_history.smoking_status, 0)
        alcohol_consumption_for_model = alcohol_mapping.get(medical_history.alcohol_consumption, 0)
        parkinsons_for_model = parkinsons_mapping.get(medical_history.family_history_parkinsons, 0)

        input_data = {
            "Age": user.age,
            "gender": gender_for_model,
            "BMI": user.bmi,
            "Smoking": smoking_status_for_model,
            "AlcoholConsumption": alcohol_consumption_for_model,
            "PhysicalActivity": PhysicalActivity2,
            "DietQuality": DietQuality,
            "SleepQuality": SleepQuality,
            "FamilyHistoryParkinsons": parkinsons_for_model,
            "TraumaticBrainInjury": TraumaticBrainInjury,
            "Hypertension": Hypertension2,
            "Diabetes": Diabetes2,
            "Depression": Depression,
            "Stroke": Stroke2,
            "SystolicBP": medical_history.systolic_bp,
            "DiastolicBP": medical_history.diastolic_bp,
            "CholesterolTotal": medical_history.cholesterol_level,
            "CholesterolLDL": medical_history.cholesterol_ldl,
            "CholesterolHDL": medical_history.cholesterol_hdl,
            "CholesterolTriglycerides": medical_history.cholesterol_triglycerides,
            "UPDRS": UPDRS,
            "MoCA": MoCA,
            "FunctionalAssessment": FunctionalAssessment,
            "Tremor": Tremor,
            "Rigidity": Rigidity,
            "Bradykinesia": Bradykinesia,
            "PosturalInstability": PosturalInstability,
            "SpeechProblems": SpeechProblems,
            "SleepDisorders": SleepDisorders,
            "Constipation": Constipation
        }
    
    elif disease_type == 'liver_disease':   
        smoking_mapping = {
            "non_smoker": 0,
            "current_smoker": 1,
            "ex_smoker": 1
        }

        alcohol_mapping = {
            "occasional": 5,
            "moderate": 10,
            "heavy": 15
        }
    
        liver_disease_mapping = {
            False: 0,
            True: 1
        }
        #print(f"Predicting disease risk for {disease_type} for user: {user.gender}")
        smoking_status_for_model = smoking_mapping.get(medical_history.smoking_status, 0)
        alcohol_consumption_for_model = alcohol_mapping.get(medical_history.alcohol_consumption, 0)
        liver_disease_for_model = liver_disease_mapping.get(medical_history.family_history_liver_disease, 0)
    
        input_data = {
            "Age": user.age,
            "gender": gender_for_model,
            "BMI": user.bmi,
            "AlcoholConsumption": alcohol_consumption_for_model,
            "Smoking": smoking_status_for_model,
            "GeneticRisk": liver_disease_for_model,
            "PhysicalActivity": PhysicalActivity3,
            "Diabetes": Diabetes3,
            "Hypertension": Hypertension3,
            "LiverFunctionTest": LiverFunctionTest
        }
    
    else:
        return HttpResponse("Invalid disease type", status=400)
    
    # Call ML model for prediction
    prediction_result = predict_disease(disease_type, input_data)

    patient_values =get_patient_values(disease_type, medical_history, input_data, user)

    # Save prediction result
    disease_prediction = DiseasePrediction.objects.create(
        patient=user,
        disease_type=disease_type,
        prediction_result=prediction_result['prediction'],
        confidence_score=prediction_result['confidence_score'],
        risk_factors=prediction_result['risk_factors'],
        severity_level=prediction_result.get('severity_level', 'Unknown'),
        recommended_treatment=prediction_result.get('recommended_treatment'),
        preventive_measures=prediction_result.get('preventive_measures'),
        patient_values=patient_values,
    )

    return render(request, 'prediction/prediction_results.html', {
        'prediction': disease_prediction,
    })

def prediction_detail(request, prediction_id):
    prediction = get_object_or_404(DiseasePrediction, id=prediction_id)
    
    return render(request, 'prediction/prediction_results.html', {
        'prediction': prediction,
    })

def get_patient_values(disease_type, medical_history, input_data, user):
    patient_values = {}
    if disease_type == 'asthma':
        patient_values = {
            "BMI": user.bmi,
            "BloodPressure": medical_history.blood_pressure,
            "SleepTime": input_data["SleepTime"],
        }
    elif disease_type == 'lung_cancer':
        patient_values = {
            "BMI": user.bmi,
            "BloodPressure": medical_history.blood_pressure,
            "HeartRate": medical_history.heart_rate,
        }
    elif disease_type == 'heart_disease':
        patient_values = {
            "BloodPressure": medical_history.blood_pressure,
            "Cholesterol": medical_history.cholesterol_level,
            "BloodGlucose": medical_history.blood_sugar,
            "HeartRate": medical_history.heart_rate,
        }
    elif disease_type == 'diabetes':
        patient_values = {
            "BMI": user.bmi,
            "HbA1c": medical_history.hba1c_level,
            "BloodGlucose": medical_history.blood_sugar,
        }
    elif disease_type == 'parkinsons':
        patient_values = {
            "BloodPressure": medical_history.blood_pressure,
            "Cholesterol": medical_history.cholesterol_level,
            "UPDRS": input_data["UPDRS"],
            "MoCA": input_data["MoCA"],
        }
    elif disease_type == 'liver_disease':
        patient_values = {
            "BMI": user.bmi,
            "Cholesterol": medical_history.cholesterol_level,
            "LiverFunctionTest": input_data["LiverFunctionTest"],
        }
    return patient_values
"""
@login_required
def book_appointment(request):
    referrer = request.GET.get('referrer', '')
    base_url = request.build_absolute_uri('/').rstrip('/')
    predictiourl= base_url + referrer
    
    form = AppointmentForm()

    return render(request, "patient/book_appointment.html", {"predictionurl": predictiourl, "form": form})"
 """

@login_required
def get_patients(request):
    if request.user.is_doctor:  # Only fetch patients if the user is a doctor
        patients = CustomUser.objects.filter(user_type="patient").values("id", "name")
        return JsonResponse({"patients": list(patients)})
    return JsonResponse({"patients": []})