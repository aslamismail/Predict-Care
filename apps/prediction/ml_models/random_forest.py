import joblib
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATASET_DIR = os.path.join(BASE_DIR, 'datasets')

def load_dataset(disease_type):
    """Load dataset for specific disease type"""
    dataset_path = os.path.join(DATASET_DIR, f'{disease_type}.csv')
    return pd.read_csv(dataset_path)

def preprocess_data(data, disease_type):
    """Preprocess input data to match the trained model feature order"""
    
    if disease_type == "asthma":
        feature_order = [
            "HeartDisease", "BMI", "Smoking", "AlcoholDrinking", "Stroke",
            "PhysicalHealth", "MentalHealth", "DiffWalking", "Gender", "Age",
            "Race", "Diabetic", "PhysicalActivity", "GenHealth", "SleepTime"
        ]

    elif disease_type == "diabetes":
        feature_order = [
            "gender", "age", "hypertension", "heart_disease",
            "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"
        ]

    elif disease_type == "heart_disease":
        feature_order = [
            "age", "gender", "chest pain type", "resting bp s", "cholesterol",
            "fasting blood sugar", "resting ecg", "max heart rate",
            "exercise angina", "oldpeak", "ST slope"
        ]

    elif disease_type == "liver_disease":
        feature_order = [
            "Age", "gender", "BMI", "AlcoholConsumption", "Smoking",
            "GeneticRisk", "PhysicalActivity", "Diabetes", "Hypertension",
            "LiverFunctionTest"
        ]

    elif disease_type == "lung_cancer":
        feature_order = [
            "gender", "age", "smoking", "yellow_fingers", "anxiety",
            "peer_pressure", "chronic_disease", "fatigue", "allergy",
            "wheezing", "alcohol_consuming", "coughing", "shortness_of_breath",
            "swallowing_difficulty", "chest_pain"
        ]

    elif disease_type == "parkinsons":
        feature_order = [
            "Age", "gender", "BMI", "Smoking", "AlcoholConsumption",
            "PhysicalActivity", "DietQuality", "SleepQuality",
            "FamilyHistoryParkinsons", "TraumaticBrainInjury",
            "Hypertension", "Diabetes", "Depression", "Stroke",
            "SystolicBP", "DiastolicBP", "CholesterolTotal", "CholesterolLDL",
            "CholesterolHDL", "CholesterolTriglycerides", "UPDRS", "MoCA",
            "FunctionalAssessment", "Tremor", "Rigidity", "Bradykinesia",
            "PosturalInstability", "SpeechProblems", "SleepDisorders",
            "Constipation"
        ]
    
    # Convert input data to DataFrame
    input_df = pd.DataFrame([data])

    # Ensure columns are in the correct order
    input_df = input_df[feature_order]

    # Convert to float (required for scaler)
    input_df = input_df.astype(float)

    # Load the trained scaler
    scaler_path = os.path.join(BASE_DIR, 'ml_models', 'trained_models', f'{disease_type}_scaler.pkl')
    scaler = joblib.load(scaler_path)

    # Scale input features
    input_scaled = scaler.transform(input_df)
    
    return input_scaled


def predict_disease(disease_type, input_data):
    """Predict disease risk using Random Forest"""
    model_path = os.path.join(BASE_DIR, 'ml_models', 'trained_models', f'{disease_type}_model.pkl')
    
    if not os.path.exists(model_path):
        print(f"⚠️ Model file not found: {model_path}")
        return {'prediction': 'Error', 'confidence_score': 0, 'risk_factors': 'N/A', 'severity_level': 'Unknown'}

    # Load pre-trained model
    model = joblib.load(model_path)
    print(f"✅ Loaded model for {disease_type}")

    # Preprocess input data
    processed_data = preprocess_data(input_data, disease_type)
    
    # Make prediction
    prediction = model.predict(processed_data)
    prediction_proba = model.predict_proba(processed_data)

    print(f"🧐 Prediction raw output: {prediction}, Probability: {prediction_proba}")
    #print("🧐 Input Data for Prediction:")
    #for key, value in input_data.items():
    #    print(f"{key}: {value}")

    return {
        'prediction': 'Positive' if prediction[0] == 1 else 'Negative',
        'confidence_score': prediction_proba[0].max(),
        'risk_factors': ', '.join(_identify_risk_factors(input_data, disease_type)),
        'severity_level': _determine_severity(prediction_proba[0].max(),input_data, disease_type),
        'recommended_treatment': _get_treatment_recommendation(disease_type, prediction[0]),
        'preventive_measures': _get_preventive_measures(disease_type)
    }

def _identify_risk_factors(input_data, disease_type):
    """Identify key risk factors from input data"""
    risk_factors = []

    if disease_type == 'diabetes':
        if input_data.get('age', 0) > 50:
            risk_factors.append('Advanced Age')
        if input_data.get('gender') == 0:
            risk_factors.append('Male Gender')
        if input_data.get('bmi', 0) > 25:
            risk_factors.append('Overweight')
        if input_data.get('heart_disease', 0) == 1:
            risk_factors.append('History of Heart Disease')
        if input_data.get('hypertension', 0) == 1:
            risk_factors.append('High Blood Pressure')
        if input_data.get('smoking_history', 0) > 0:  
            risk_factors.append('Smoking History')
        if input_data.get('HbA1c_level', 0) >= 5.7:
            risk_factors.append('Elevated HbA1c Level')
        if input_data.get('blood_glucose_level', 0) > 125:
            risk_factors.append('High Blood Glucose Level')

    elif disease_type == 'heart_disease':
        if input_data.get('age', 0) > 45:
            risk_factors.append('Advanced Age')
        if input_data.get('gender') == 0:  
            risk_factors.append('Male Gender')
        if input_data.get('resting bp s', 0) > 130:
            risk_factors.append('High Blood Pressure')
        if input_data.get('cholesterol', 0) > 200:
            risk_factors.append('High Cholesterol Level')
        if input_data.get('fasting blood sugar', 0) > 100:
            risk_factors.append('High Blood Sugar')
        if input_data.get('resting ecg', 0) > 0:  
            risk_factors.append('Abnormal Resting ECG')
        if input_data.get('exercise angina', 0) == 1:  
            risk_factors.append('Exercise-Induced Angina')
        if input_data.get('ST slope', 0) in [1, 2]:  
            risk_factors.append('Abnormal ST Slope')
    
    elif disease_type == 'liver_disease':
        if input_data.get('Age', 0) > 50:
            risk_factors.append('Advanced Age')
        if input_data.get('gender') == 0:
            risk_factors.append('Male Gender')
        if input_data.get('BMI', 0) > 30:
            risk_factors.append('Obesity')
        if input_data.get('AlcoholConsumption', 0) >= 10:  
            risk_factors.append('Regular Alcohol Consumption')
        if input_data.get('Smoking', 0) == 1:  
            risk_factors.append('Smoking History')
        if input_data.get('GeneticRisk', 0) == 1:
            risk_factors.append('Family History')
        if input_data.get('PhysicalActivity', 0) <= 3:  
            risk_factors.append('Sedentary Lifestyle')
        if input_data.get('Diabetes', 0) == 1:
            risk_factors.append('Diabetes')
        if input_data.get('Hypertension', 0) == 1:
            risk_factors.append('High Blood Pressure')

    elif disease_type == 'lung_cancer':
        if input_data.get('age', 0) > 50:
            risk_factors.append('Advanced Age')
        if input_data.get('gender') == 0:  
            risk_factors.append('Male Gender')
        if input_data.get('smoking', 1) == 2:
            risk_factors.append('Smoking History')
        if input_data.get('chronic_disease', 1) == 2:
            risk_factors.append('Chronic Respiratory Disease')
        if input_data.get('allergy', 1) == 2:
            risk_factors.append('Respiratory Allergies')
        if input_data.get('alcohol_consuming', 1) == 2:
            risk_factors.append('Regular Alcohol Consumption')
        if input_data.get('chest_pain', 1) == 2:
            risk_factors.append('Unexplained Chest Pain')

    elif disease_type == 'parkinsons':
        if input_data.get('Age', 0) > 60:
            risk_factors.append('Advanced Age')
        if input_data.get('gender') == 0:  
            risk_factors.append('Male Gender')
        if input_data.get('BMI', 0) > 25:
            risk_factors.append('Overweight')
        if input_data.get('Smoking', 0) == 1:
            risk_factors.append('Smoking History')
        if input_data.get('AlcoholConsumption', 0) >= 10:
            risk_factors.append('Regular Alcohol Consumption')
        if input_data.get('PhysicalActivity', 0) <= 3:
            risk_factors.append('Sedentary Lifestyle')
        if input_data.get('FamilyHistoryParkinsons', 0) == 1:
            risk_factors.append('Family History')
        if input_data.get('Hypertension', 0) == 1:
            risk_factors.append('High Blood Pressure')
        if input_data.get('Diabetes', 0) == 1:
            risk_factors.append('Diabetes')
        if input_data.get('CholesterolTotal', 0) > 200:
            risk_factors.append('High Cholesterol Level')

    elif disease_type == 'asthma':
        if input_data.get('Age', 0) < 18 or input_data.get('Age', 0) > 50:
            risk_factors.append('Age Factor (Children or Older Adults)')
        if input_data.get('Gender') == 0:  
            risk_factors.append('Male Gender')
        if input_data.get('HeartDisease', 0) == 1:
            risk_factors.append('Heart Disease')
        if input_data.get('BMI', 0) > 25:
            risk_factors.append('Overweight')
        if input_data.get('Smoking', 0) == 1:
            risk_factors.append('Smoking History')
        if input_data.get('AlcoholDrinking', 0) == 1:
            risk_factors.append('Regular Alcohol Consumption')
        if input_data.get('Race') == 1 or input_data.get('Race') == 3 or input_data.get('Race') == 5:
            risk_factors.append('Higher Risk in Certain Ethnic Groups')
        if input_data.get('Diabetic', 0) == 1:
            risk_factors.append('Diabetes')
        if input_data.get('PhysicalActivity', 0) == 0:
            risk_factors.append('Sedentary Lifestyle')

    return risk_factors

def _determine_severity(prediction_proba, input_data, disease_type):
    """
    Determine severity based on both model confidence and medical risk factors.
    """
    confidence = np.max(prediction_proba)  # Get highest probability score
    severity = "Low Risk"
    high_risk_conditions = False

    if disease_type == 'diabetes':
        high_risk_conditions = (
            (input_data['HbA1c_level'] > 9) or
            (input_data['blood_glucose_level'] > 250) or
            (input_data['bmi'] > 35)
        )
    elif disease_type == 'heart_disease':
        high_risk_conditions = (
            (input_data['resting bp s'] > 180) or
            (input_data['cholesterol'] > 300) or
            (input_data['max heart rate'] < 80) or
            (input_data['oldpeak'] > 2)
        )
    elif disease_type == 'liver_disease':
        high_risk_conditions = (
            (input_data['LiverFunctionTest'] > 100) or
            (input_data['AlcoholConsumption'] >= 10) or
            (input_data['BMI'] > 35)
        )
    elif disease_type == 'lung_cancer':
        high_risk_conditions = (
            (input_data['smoking'] > 1) or
            (input_data['age'] > 70) or
            (input_data['chronic_disease'] == 2 and input_data['chest_pain'] == 2)
        )
    elif disease_type == 'parkinsons':
        high_risk_conditions = (
            (input_data['Age'] > 70) or
            (input_data['FamilyHistoryParkinsons'] == 1) or
            (input_data['PhysicalActivity'] <= 3)
        )
    elif disease_type == 'asthma':
        high_risk_conditions = (
            (input_data['BMI'] > 35) or
            (input_data['Smoking'] == 1) or
            (input_data['HeartDisease'] == 1 and input_data['Diabetic'] == 1)
        )

    if confidence >= 0.7 and high_risk_conditions:
        severity = "High Risk"
    elif confidence > 0.4:
        severity = "Moderate Risk"
    else:
        severity = "Low Risk"

    return severity

def _get_treatment_recommendation(disease_type, prediction):
    """Generate treatment recommendations"""
    if prediction == 0:
        recommendations = {
            'diabetes': 'Maintain Healthy Diet, Regular Exercise, Annual Checkups',
            'heart_disease': 'Maintain Heart Health, Balanced Diet, Regular Exercise',
            'lung_cancer': 'Avoid Smoking, Regular Screenings, Healthy Lifestyle',
            'asthma': 'Maintain Clean Air, Exercise Caution, Monitor Symptoms',
            'liver_disease': 'Healthy Diet, Avoid Alcohol, Routine Checkups',
            'parkinsons': 'Stay Active, Healthy Diet, Monitor Symptoms Regularly'
        }
    elif prediction == 1:
        recommendations = {
            'diabetes': 'Consult Endocrinologist, Monitor Blood Sugar, Lifestyle Changes',
            'heart_disease': 'Cardiac Consultation, Medication, Lifestyle Modifications',
            'lung_cancer': 'Oncology Referral, Advanced Diagnostic Tests, Possible Biopsy',
            'asthma': 'Pulmonologist Consultation, Use Prescribed Inhalers, Avoid Triggers',
            'liver_disease': 'Hepatologist Consultation, Liver Function Tests, Medication',
            'parkinsons': 'Neurologist Consultation, Physical Therapy, Medication Management'
        }
    else:
        recommendations = {'default': 'No specific recommendation available'}

    return recommendations.get(disease_type, 'General Medical Consultation')

def _get_preventive_measures(disease_type):
    """Generate preventive measures"""
    measures = {
        'diabetes': 'Maintain Healthy Diet, Regular Exercise, Weight Management',
        'heart_disease': 'Regular Exercise, Low Cholesterol Diet, Stress Management',
        'lung_cancer': 'Avoid Smoking, Reduce Pollution Exposure, Regular Checkups',
        'asthma': 'Avoid Triggers, Use Air Purifiers, Stay Hydrated',
        'liver_disease': 'Limit Alcohol Intake, Maintain Healthy Weight, Get Vaccinated for Hepatitis',
        'parkinsons': 'Stay Physically Active, Maintain Brain Health, Reduce Head Trauma Risk'
    }
    return measures.get(disease_type, 'Maintain General Health')
