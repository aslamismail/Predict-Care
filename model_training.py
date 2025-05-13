import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def generate_datasets():
    """Generate sample datasets for each disease"""
    
    n_records = 50000
    
    # Diabetes Dataset
    diabetes_data = {
        'age': np.random.randint(20, 90, n_records),
        'gender': np.random.choice(['M', 'F'], n_records),
        'glucose': np.round(np.random.uniform(70, 200, n_records),1),
        'blood_pressure': np.round(np.random.uniform(60, 180, n_records),1),
        'insulin': np.round(np.random.uniform(0, 300, n_records),1),
        'bmi': np.round(np.random.uniform(18.5, 40, n_records),1),
        'diabetes_pedigree': np.round(np.random.uniform(0, 2.5, n_records),1),
        'target': np.random.choice([0, 1], n_records, p=[0.65, 0.35])  # 35% positive cases
    }
    
    # Heart Disease Dataset
    heart_data = {
        'age': np.random.randint(20, 90, n_records),
        'gender': np.random.choice(['M', 'F'], n_records),
        'chest_pain_type': np.random.randint(0, 4, n_records),
        'resting_blood_pressure': np.round(np.random.uniform(90, 200, n_records),1),
        'cholesterol': np.round(np.random.uniform(120, 400, n_records),1),
        'fasting_blood_sugar': np.random.choice([0, 1], n_records),
        'max_heart_rate': np.round(np.random.uniform(60, 202, n_records),1),
        'exercise_induced_angina': np.random.choice([0, 1], n_records),
        'target': np.random.choice([0, 1], n_records, p=[0.6, 0.4])  # 40% positive cases
    }
    
    # Cancer Dataset
    cancer_data = {
        'age': np.random.randint(20, 90, n_records),
        'gender': np.random.choice(['M', 'F'], n_records),
        'tumor_size': np.round(np.random.uniform(0, 10, n_records),1),
        'tumor_grade': np.random.randint(1, 4, n_records),
        'lymph_nodes': np.random.randint(0, 10, n_records),
        'metastasis': np.random.choice([0, 1], n_records),
        'cancer_type': np.random.choice(['type1', 'type2', 'type3'], n_records),
        'target': np.random.choice([0, 1], n_records, p=[0.7, 0.3])  # 30% positive cases
    }
    
    # Parkinsons Dataset
    parkinsons_data = {
        'age': np.random.randint(20, 90, n_records),
        'gender': np.random.choice(['M', 'F'], n_records),
        'tremor': np.round(np.random.uniform(0, 10, n_records),1),
        'rigidity': np.round(np.random.uniform(0, 10, n_records),1),
        'balance': np.round(np.random.uniform(0, 10, n_records),1),
        'speech_changes': np.round(np.random.uniform(0, 10, n_records),1),
        'target': np.random.choice([0, 1], n_records, p=[0.75, 0.25])  # 25% positive cases
    }

     # Arthritis Dataset
    arthritis_data = {
        'age': np.random.randint(20, 90, n_records),
        'gender': np.random.choice(['M', 'F'], n_records),
        'joint_pain': np.round(np.random.uniform(0, 10, n_records),1),  # Scale 0-10 for pain severity
        'swelling': np.round(np.random.uniform(0, 10, n_records),1),  # Scale 0-10 for swelling severity
        'stiffness': np.round(np.random.uniform(0, 10, n_records),1),  # Scale 0-10 for stiffness severity
        'family_history': np.random.choice([0, 1], n_records),  # 0 = no history, 1 = family history
        'target': np.random.choice([0, 1], n_records, p=[0.6, 0.4])  # 40% positive cases
    }
    
    # Asthma Dataset
    asthma_data = {
        'age': np.random.randint(20, 90, n_records),
        'gender': np.random.choice(['M', 'F'], n_records),
        'wheezing': np.round(np.random.uniform(0, 10, n_records),1),  # Scale 0-10 for wheezing severity
        'shortness_of_breath': np.round(np.random.uniform(0, 10, n_records),1),
        'cough_frequency': np.round(np.random.uniform(0, 10, n_records),1),
        'allergy_history': np.random.choice([0, 1], n_records),  # 0 = no allergy, 1 = allergy history
        'target': np.random.choice([0, 1], n_records, p=[0.7, 0.3])  # 30% positive cases
    }
    
    # Liver Disease Dataset
    liver_data = {
        'age': np.random.randint(20, 90, n_records),
        'gender': np.random.choice(['M', 'F'], n_records),
        'bilirubin': np.round(np.random.uniform(0.1, 2.0, n_records),1),  # Normal range 0.1-1.2 mg/dL
        'alkaline_phosphatase': np.round(np.random.uniform(20, 140, n_records),1),  # Normal range 20-140 U/L
        'albumin': np.round(np.random.uniform(3.5, 5.0, n_records),1),  # Normal range 3.5-5.0 g/dL
        'target': np.random.choice([0, 1], n_records, p=[0.65, 0.35])  # 35% positive cases
    }
    
    # Create DataFrames
    datasets = {
        'diabetes': pd.DataFrame(diabetes_data),
        'heart_disease': pd.DataFrame(heart_data),
        'cancer': pd.DataFrame(cancer_data),
        'parkinsons': pd.DataFrame(parkinsons_data),
        'arthritis': pd.DataFrame(arthritis_data),
        'asthma': pd.DataFrame(asthma_data),
        'liver_disease': pd.DataFrame(liver_data)
    }
    
    # Save datasets
    for name, df in datasets.items():
        df.to_csv(f'datasets/{name}.csv', index=False)
    
    return datasets

def preprocess_dataset(df):
    """Preprocess the dataset for training"""
    
    # Handle categorical variables
    categorical_columns = df.select_dtypes(include=['object']).columns
    for column in categorical_columns:
        df[column] = pd.Categorical(df[column]).codes
    
    # Split features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_models(datasets):
    """Train Random Forest models for each disease"""
    
    models = {}
    scalers = {}
    performance = {}
    
    for disease, df in datasets.items():
        print(f"\nTraining model for {disease}...")
        
        # Preprocess data
        X_train, X_test, y_train, y_test, scaler = preprocess_dataset(df)
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        # Store results
        models[disease] = model
        scalers[disease] = scaler
        performance[disease] = {
            'accuracy': accuracy,
            'report': report
        }
        
        # Save model and scaler
        if not os.path.exists('ml_models/trained_models'):
            os.makedirs('ml_models/trained_models')
        
        joblib.dump(model, f'ml_models/trained_models/{disease}_model.pkl')
        joblib.dump(scaler, f'ml_models/trained_models/{disease}_scaler.pkl')
        
        print(f"{disease} model accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(report)
    
    return models, scalers, performance

def main():
    """Main function to generate datasets and train models"""
    
    # Create datasets directory if it doesn't exist
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    
    # Generate and save datasets
    print("Generating datasets...")
    datasets = generate_datasets()
    
    # Train and save models
    print("\nTraining models...")
    models, scalers, performance = train_models(datasets)
    
    print("\nModel training complete!")
    return models, scalers, performance

if __name__ == "__main__":
    main()
