import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

class SymptomPredictor:
    """
    Machine Learning model for predicting diseases based on symptoms
    """
    def __init__(self):
        self.model = None
        self.symptom_mapping = {
            'fever': 0, 'cough': 1, 'headache': 2, 'fatigue': 3,
            'sore throat': 4, 'difficulty breathing': 5, 'chest pain': 6,
            'body ache': 7, 'nausea': 8, 'diarrhea': 9
        }
        self.disease_mapping = {
            0: 'Common Cold',
            1: 'Respiratory Infection',
            2: 'Influenza',
            3: 'COVID-19',
            4: 'Bronchitis',
            5: 'Pneumonia',
            6: 'Asthma',
            7: 'Allergies',
            8: 'Gastroenteritis',
            9: 'Migraine'
        }
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model or create a new one"""
        model_path = 'ml_models/trained_models/disease_predictor.pkl'
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.train_model()
    
    def train_model(self):
        """Train the model with sample data"""
        X = np.random.rand(100, 10)
        y = np.random.randint(0, 10, 100)
        self.model.fit(X, y)
    
    def predict(self, symptoms_text):
        """Predict disease from symptom description"""
        features = self.extract_features(symptoms_text)
        prediction = self.model.predict([features])[0]
        confidence = float(self.model.predict_proba([features])[0].max())
        
        disease = self.disease_mapping.get(prediction, 'Unknown')
        risk_level = self.calculate_risk(disease)
        
        return {
            'disease': disease,
            'confidence': confidence,
            'risk_level': risk_level,
            'recommendations': self.get_recommendations(disease)
        }
    
    def extract_features(self, symptoms_text):
        """Extract features from symptom text"""
        features = np.zeros(len(self.symptom_mapping))
        text_lower = symptoms_text.lower()
        
        for symptom, idx in self.symptom_mapping.items():
            if symptom in text_lower:
                features[idx] = 1
        
        return features
    
    def calculate_risk(self, disease):
        """Calculate risk level for the disease"""
        high_risk = ['Pneumonia', 'COVID-19', 'Asthma']
        medium_risk = ['Respiratory Infection', 'Influenza', 'Bronchitis']
        
        if disease in high_risk:
            return 'High'
        elif disease in medium_risk:
            return 'Medium'
        else:
            return 'Low'
    
    def get_recommendations(self, disease):
        """Get health recommendations for the disease"""
        recommendations = {
            'Common Cold': ['Stay hydrated', 'Rest well', 'Use tissues', 'Avoid close contact'],
            'Respiratory Infection': ['See a doctor', 'Take antibiotics if prescribed', 'Rest', 'Drink fluids'],
            'Influenza': ['Seek medical attention', 'Rest', 'Antiviral medication', 'Stay isolated'],
            'COVID-19': ['Get tested immediately', 'Isolate yourself', 'Monitor oxygen levels', 'Contact doctor'],
            'Pneumonia': ['Emergency medical care', 'Antibiotics', 'Rest', 'Oxygen therapy'],
        }
        return recommendations.get(disease, ['Consult with a healthcare professional', 'Monitor symptoms', 'Rest well'])

# Create global predictor instance
predictor = SymptomPredictor()

def predict_disease(symptoms):
    """Public function to predict disease"""
    return predictor.predict(symptoms)
