"""
Database configuration and models for AI Health Assistant
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class SymptomAnalysis(db.Model):
    """Store symptom analysis results"""
    __tablename__ = 'symptom_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    user_symptoms = db.Column(db.Text, nullable=False)  # JSON list of symptoms
    primary_disease = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)  # High, Medium, Low
    emergency_alert = db.Column(db.Boolean, default=False)
    all_results = db.Column(db.Text, nullable=False)  # JSON of top 3 results
    recommendations = db.Column(db.Text, nullable=False)  # JSON advice
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symptoms': json.loads(self.user_symptoms),
            'primary_disease': self.primary_disease,
            'confidence': self.confidence,
            'risk_level': self.risk_level,
            'emergency_alert': self.emergency_alert,
            'results': json.loads(self.all_results),
            'recommendations': json.loads(self.recommendations),
            'created_at': self.created_at.isoformat()
        }

class MedicineVerification(db.Model):
    """Store medicine verification results"""
    __tablename__ = 'medicine_verification'
    
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(255), nullable=False)
    is_authentic = db.Column(db.Boolean, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    ocr_data = db.Column(db.Text, nullable=False)  # JSON of OCR results
    image_analysis = db.Column(db.Text, nullable=False)  # JSON of analysis
    decision_logic = db.Column(db.Text, nullable=False)  # JSON scores
    recommendation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_filename': self.image_filename,
            'is_authentic': self.is_authentic,
            'confidence': self.confidence,
            'ocr_data': json.loads(self.ocr_data),
            'image_analysis': json.loads(self.image_analysis),
            'decision_logic': json.loads(self.decision_logic),
            'recommendation': self.recommendation,
            'created_at': self.created_at.isoformat()
        }


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
