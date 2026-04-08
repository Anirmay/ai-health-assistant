"""
Comprehensive medicine database with real Indian pharmaceutical brands
"""

# Real medicines database - organized by category
REAL_MEDICINES = {
    # Fever/Pain Relief
    "paracetamol": {"brand": "Crocin", "manufacturer": "GSK", "category": "Fever/Pain"},
    "crocin": {"brand": "Crocin", "manufacturer": "GSK", "category": "Fever/Pain"},
    "ibuprofen": {"brand": "Brufen", "manufacturer": "Abbott", "category": "Pain Reliever"},
    "aspirin": {"brand": "Ecosprin", "manufacturer": "USV", "category": "Antiplatelet"},
    "diclofenac": {"brand": "Voltaren", "manufacturer": "Novartis", "category": "Pain Reliever"},
    "naproxen": {"brand": "Naprosyn", "manufacturer": "Cipla", "category": "Pain Reliever"},
    
    # Cough & Cold
    "cetirizine": {"brand": "Allergin", "manufacturer": "Cipla", "category": "Antihistamine"},
    "loratadine": {"brand": "Claritin", "manufacturer": "Schering", "category": "Antihistamine"},
    "codeine": {"brand": "Codeinal", "manufacturer": "Cipla", "category": "Cough Suppressant"},
    "dextromethorphan": {"brand": "Robitussin", "manufacturer": "Wyeth", "category": "Cough"},
    "guaifenesin": {"brand": "Mucinex", "manufacturer": "Reckitt", "category": "Expectorant"},
    
    # Antibiotics
    "amoxicillin": {"brand": "Amoxil", "manufacturer": "GSK", "category": "Antibiotic"},
    "azithromycin": {"brand": "Zithromax", "manufacturer": "Pfizer", "category": "Antibiotic"},
    "ciprofloxacin": {"brand": "Cipro", "manufacturer": "Cipla", "category": "Antibiotic"},
    "cefixime": {"brand": "Suprax", "manufacturer": "Lupin", "category": "Antibiotic"},
    "metronidazole": {"brand": "Flagyl", "manufacturer": "Abbott", "category": "Antibiotic"},
    
    # Digestive
    "omeprazole": {"brand": "Losec", "manufacturer": "Astrazeneca", "category": "Acid Reducer"},
    "ranitidine": {"brand": "Zantac", "manufacturer": "GSK", "category": "Acid Reducer"},
    "metoclopramide": {"brand": "Maxolon", "manufacturer": "Cipla", "category": "Antiemetic"},
    "domperidone": {"brand": "Motilium", "manufacturer": "Janssen", "category": "Antiemetic"},
    "loperamide": {"brand": "Imodium", "manufacturer": "McNeill", "category": "Antidiarrheal"},
    
    # Blood Pressure
    "amlodipine": {"brand": "Norvasc", "manufacturer": "Pfizer", "category": "Hypertension"},
    "enalapril": {"brand": "Enacard", "manufacturer": "Merck", "category": "Hypertension"},
    "lisinopril": {"brand": "Lisinopril", "manufacturer": "Cipla", "category": "Hypertension"},
    "metoprolol": {"brand": "Betaloc", "manufacturer": "AstraZeneca", "category": "Beta Blocker"},
    
    # Diabetes
    "metformin": {"brand": "Glucophage", "manufacturer": "Bristol", "category": "Diabetes"},
    "glipizide": {"brand": "Glucotrol", "manufacturer": "Pfizer", "category": "Diabetes"},
    "insulin": {"brand": "Humalog", "manufacturer": "Lilly", "category": "Diabetes"},
    
    # Vitamins & Supplements
    "vitamin_b12": {"brand": "Cyanocobalamin", "manufacturer": "Various", "category": "Supplement"},
    "vitamin_d3": {"brand": "Cholecalciferol", "manufacturer": "Various", "category": "Supplement"},
    "multivitamin": {"brand": "Revital", "manufacturer": "Merck", "category": "Supplement"},
    "iron": {"brand": "Feroglobin", "manufacturer": "Various", "category": "Supplement"},
    "calcium": {"brand": "Caltrate", "manufacturer": "Pfizer", "category": "Supplement"},
    
    # Allergy & Immunology
    "hydrocortisone": {"brand": "Cortisol", "manufacturer": "Various", "category": "Steroid"},
    "prednisolone": {"brand": "Predonine", "manufacturer": "Cipla", "category": "Steroid"},
    "desloratadine": {"brand": "Aerius", "manufacturer": "Schering", "category": "Antihistamine"},
    
    # Sleep
    "melatonin": {"brand": "Melatonin", "manufacturer": "Various", "category": "Sleep Aid"},
    "zolpidem": {"brand": "Ambien", "manufacturer": "Sanofi", "category": "Sleep Aid"},
    
    # Anxiety & Depression
    "sertraline": {"brand": "Zoloft", "manufacturer": "Pfizer", "category": "Antidepressant"},
    "fluoxetine": {"brand": "Prozac", "manufacturer": "Lilly", "category": "Antidepressant"},
    "escitalopram": {"brand": "Lexapro", "manufacturer": "Forest", "category": "Antidepressant"},
    "alprazolam": {"brand": "Xanax", "manufacturer": "Pfizer", "category": "Anxiolytic"},
    
    # Thyroid
    "levothyroxine": {"brand": "Synthroid", "manufacturer": "Abbott", "category": "Thyroid"},
    
    # Cholesterol
    "atorvastatin": {"brand": "Lipitor", "manufacturer": "Pfizer", "category": "Statin"},
    "simvastatin": {"brand": "Zocor", "manufacturer": "Merck", "category": "Statin"},
    
    # Joint Pain
    "glucosamine": {"brand": "Arthoflex", "manufacturer": "Various", "category": "Joint"},
    "chondroitin": {"brand": "Chondro", "manufacturer": "Various", "category": "Joint"},
}

# Common fake medicine indicators
FAKE_MEDICINE_INDICATORS = {
    "spelling_errors": ["Paracetamol misspelled", "Brand name incorrect"],
    "packaging_issues": ["Blurred text", "Poor print quality", "Wrong colors"],
    "hologram_missing": ["No hologram", "Fake hologram", "Hologram easily peels"],
    "batch_number_issues": ["Invalid format", "Repeated numbers", "Too short"],
    "barcode_issues": ["Barcode doesn't scan", "Damaged barcode", "Incorrect format"],
}

def verify_medicine_in_database(medicine_name: str) -> bool:
    """Check if medicine exists in real database"""
    return medicine_name.lower() in REAL_MEDICINES

def get_medicine_info(medicine_name: str) -> dict:
    """Get medicine information"""
    med = REAL_MEDICINES.get(medicine_name.lower())
    if med:
        return {
            "medicine": medicine_name,
            "brand": med["brand"],
            "manufacturer": med["manufacturer"],
            "category": med["category"],
            "found": True
        }
    return {
        "medicine": medicine_name,
        "found": False
    }
