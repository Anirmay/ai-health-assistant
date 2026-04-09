"""
NLP-based Symptom Mapper
Converts natural language symptom inputs to known symptoms using semantic similarity
"""

import numpy as np
from difflib import SequenceMatcher
import warnings

# Try to import sentence-transformers, fallback to difflib if not available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    warnings.warn("sentence-transformers not installed. Falling back to fuzzy matching.")

from sklearn.metrics.pairwise import cosine_similarity


class SymptomMapper:
    """Maps natural language symptom inputs to known symptoms using NLP"""
    
    def __init__(self):
        """Initialize the symptom mapper"""
        self.known_symptoms = [
            'fever', 'cough', 'headache', 'fatigue', 'sore throat',
            'body ache', 'nausea', 'diarrhea', 'shortness of breath',
            'chest pain', 'cold', 'flu', 'covid', 'anxiety',
            'migraine', 'anemia', 'asthma', 'heart disease',
            'pneumonia', 'gastritis', 'dengue', 'tuberculosis',
            'loss of consciousness', 'hair loss', 'difficulty breathing',
            'severe bleeding', 'seizure', 'poisoning'
        ]
        
        self.model = None
        self.symptom_embeddings = None
        self.similarity_threshold = 0.6  # Minimum similarity to accept match
        
        # Try to load the sentence transformer model
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                # Using lightweight model: all-MiniLM-L6-v2 (~22MB, very fast)
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.compute_symptom_embeddings()
                self.nlp_enabled = True
            except Exception as e:
                print(f"[WARNING] Failed to load sentence-transformers: {str(e)}")
                self.nlp_enabled = False
        else:
            self.nlp_enabled = False
    
    def compute_symptom_embeddings(self):
        """Pre-compute embeddings for all known symptoms"""
        if self.model:
            self.symptom_embeddings = self.model.encode(
                self.known_symptoms,
                convert_to_numpy=True
            )
    
    def map_symptom_nlp(self, user_input: str):
        """
        Map user input to known symptom using NLP (semantic similarity)
        
        Args:
            user_input: Natural language symptom description
            
        Returns:
            {
                'mapped_symptom': str,
                'confidence': float (0-1),
                'method': 'nlp',
                'alternatives': [list of alternatives]
            }
        """
        if not self.nlp_enabled or not self.model:
            return None
        
        try:
            # Embed user input
            user_embedding = self.model.encode(
                [user_input.lower()],
                convert_to_numpy=True
            )
            
            # Calculate cosine similarity with all known symptoms
            similarities = cosine_similarity(user_embedding, self.symptom_embeddings)[0]
            
            # Get top 3 matches
            top_indices = np.argsort(similarities)[::-1][:3]
            
            top_symptom_idx = top_indices[0]
            top_similarity = similarities[top_symptom_idx]
            
            # Get alternatives
            alternatives = []
            for idx in top_indices[1:]:
                sim = similarities[idx]
                if sim > 0.3:  # Only include reasonable alternatives
                    alternatives.append({
                        'symptom': self.known_symptoms[idx],
                        'confidence': float(round(sim, 2))
                    })
            
            return {
                'mapped_symptom': self.known_symptoms[top_symptom_idx],
                'confidence': float(round(top_similarity, 2)),
                'method': 'nlp',
                'alternatives': alternatives,
                'user_input': user_input
            }
        
        except Exception as e:
            print(f"[ERROR] NLP mapping failed: {str(e)}")
            return None
    
    def map_symptom_fuzzy(self, user_input: str):
        """
        Fallback: Map using fuzzy string matching (difflib)
        
        Args:
            user_input: Natural language symptom description
            
        Returns:
            {
                'mapped_symptom': str,
                'confidence': float (0-1),
                'method': 'fuzzy',
                'alternatives': [list of alternatives]
            }
        """
        user_input_lower = user_input.lower()
        
        # Calculate similarity with all known symptoms
        similarities = {}
        for symptom in self.known_symptoms:
            ratio = SequenceMatcher(None, user_input_lower, symptom).ratio()
            similarities[symptom] = ratio
        
        # Get best match
        best_symptom = max(similarities.items(), key=lambda x: x[1])
        best_match = best_symptom[0]
        best_confidence = best_symptom[1]
        
        # Get alternatives
        alternatives = []
        sorted_symptoms = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        for symptom, confidence in sorted_symptoms[1:3]:
            if confidence > 0.4:
                alternatives.append({
                    'symptom': symptom,
                    'confidence': float(round(confidence, 2))
                })
        
        return {
            'mapped_symptom': best_match,
            'confidence': float(round(best_confidence, 2)),
            'method': 'fuzzy',
            'alternatives': alternatives,
            'user_input': user_input
        }
    
    def map_symptom(self, user_input: str):
        """
        Map symptom using NLP first, fallback to fuzzy matching
        
        Args:
            user_input: Natural language symptom description
            
        Returns:
            Mapping result with mapped symptom and confidence
        """
        # Exact match first (fastest)
        user_lower = user_input.lower().strip()
        if user_lower in self.known_symptoms:
            return {
                'mapped_symptom': user_lower,
                'confidence': 1.0,
                'method': 'exact',
                'alternatives': [],
                'user_input': user_input
            }
        
        # Try NLP mapping
        if self.nlp_enabled:
            result = self.map_symptom_nlp(user_input)
            if result and result['confidence'] >= self.similarity_threshold:
                return result
        
        # Fallback to fuzzy matching
        return self.map_symptom_fuzzy(user_input)
    
    def map_symptoms(self, symptoms: list):
        """
        Map multiple symptoms (user can provide comma-separated or list)
        
        Args:
            symptoms: List of symptom strings or comma-separated string
            
        Returns:
            List of mappings
        """
        if isinstance(symptoms, str):
            symptom_list = [s.strip() for s in symptoms.split(',')]
        else:
            symptom_list = symptoms
        
        mappings = []
        for symptom in symptom_list:
            if symptom.strip():
                mapping = self.map_symptom(symptom.strip())
                mappings.append(mapping)
        
        return mappings
    
    def get_mapping_summary(self, mappings: list):
        """
        Generate a human-readable summary of symptom mappings
        
        Args:
            mappings: List of mapping results
            
        Returns:
            Summary string and confidence assessment
        """
        if not mappings:
            return "No symptoms mapped", 0.0
        
        mapped_symptoms = [m['mapped_symptom'] for m in mappings]
        avg_confidence = np.mean([m['confidence'] for m in mappings])
        
        summary_parts = []
        for mapping in mappings:
            user_input = mapping['user_input']
            mapped = mapping['mapped_symptom']
            confidence = mapping['confidence']
            method = mapping['method']
            
            if user_input.lower() != mapped.lower():
                summary_parts.append(
                    f'✓ "{user_input}" → "{mapped}" ({int(confidence*100)}% - {method})'
                )
            else:
                summary_parts.append(f'✓ Recognized: "{mapped}"')
        
        summary = '\n'.join(summary_parts)
        
        return summary, avg_confidence, mapped_symptoms
    
    def add_custom_symptom(self, symptom: str):
        """
        Add a custom symptom to the known symptoms list
        
        Args:
            symptom: New symptom to add
        """
        symptom_lower = symptom.lower().strip()
        if symptom_lower not in self.known_symptoms:
            self.known_symptoms.append(symptom_lower)
            # Recompute embeddings if NLP is enabled
            if self.nlp_enabled:
                self.compute_symptom_embeddings()


# Create global mapper instance
symptom_mapper = SymptomMapper()


def map_user_symptoms(user_input: str):
    """Public function to map user symptoms"""
    return symptom_mapper.map_symptoms(user_input)


def get_symptom_mapping_summary(mappings: list):
    """Public function to get summary of mappings"""
    return symptom_mapper.get_mapping_summary(mappings)
