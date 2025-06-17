# policy_data.py

policies = [
    {
        "name": "Basic Health Plan",
        "age_range": (18, 55),
        "type": "individual",
        "premium": 150,
        "coverage": "Essential in-patient coverage, emergency services only.",
        "special_features": [],
    },
    {
        "name": "Family Health Plus Plan",
        "age_range": (0, 55),
        "type": "family",
        "premium": 350,
        "coverage": "In-patient, out-patient, specialist visits, and emergency transport.",
        "special_features": ["maternity"],
    },
    {
        "name": "Comprehensive Health & Wellness Plan",
        "age_range": (0, 100),
        "type": "both",
        "premium": 500,
        "coverage": "All Family Health Plus benefits + mental health, wellness, and preventive care.",
        "special_features": ["mental health", "wellness", "maternity"],
    },
    {
        "name": "Senior Health Security Plan",
        "age_range": (55, 100),
        "type": "individual",
        "premium": 600,
        "coverage": "Senior-specific coverage: long-term care, vision, dental, routine prescriptions.",
        "special_features": ["dental", "vision"],
    }
]

add_ons = {
    "dental": {
        "name": "Dental & Vision Add-On",
        "cost": 50,
        "available_in": ["Basic Health Plan", "Family Health Plus Plan", "Comprehensive Health & Wellness Plan"],
    },
    "maternity": {
        "name": "Maternity & Newborn Care Add-On",
        "cost": 75,
        "available_in": ["Family Health Plus Plan", "Comprehensive Health & Wellness Plan"],
    },
    "travel": {
        "name": "International Travel Medical Insurance",
        "cost": 40,
        "available_in": ["Basic Health Plan", "Family Health Plus Plan", "Comprehensive Health & Wellness Plan", "Senior Health Security Plan"],
    }
}
