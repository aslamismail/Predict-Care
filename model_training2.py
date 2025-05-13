import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def load_datasets():
    """
    Load real-world datasets for different chronic diseases.
    Each dataset should have a 'target' column as the label.
    """
    dataset_files = {
        'diabetes': 'datasets/diabetes.csv',
        'heart_disease': 'datasets/heart_disease.csv',
        'lung_cancer': 'datasets/lung_cancer.csv',
        'asthma': 'datasets/asthma.csv',
        'liver_disease': 'datasets/liver_disease.csv',
        'parkinsons': 'datasets/parkinsons.csv',
    }
    
    datasets = {}
    for disease, file_path in dataset_files.items():
        if os.path.exists(file_path):
            print(f"Loading {disease} dataset...")
            datasets[disease] = pd.read_csv(file_path)
        else:
            print(f"Dataset not found for {disease}: {file_path}")
    
    return datasets

def preprocess_dataset(df):
    """
    Preprocess the dataset for training.
    """
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
    """
    Train Random Forest models for each disease using real-world datasets.
    """
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
    """
    Main function to load datasets and train models.
    """
    # Load datasets
    print("Loading datasets...")
    datasets = load_datasets()
    
    if not datasets:
        print("No datasets found. Please ensure the dataset files are in the 'datasets/' directory.")
        return
    
    # Train and save models
    print("\nTraining models...")
    models, scalers, performance = train_models(datasets)
    
    print("\nModel training complete!")
    return models, scalers, performance

if __name__ == "__main__":
    main()
