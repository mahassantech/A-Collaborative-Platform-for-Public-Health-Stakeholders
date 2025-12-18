
ROLE_CHOICES = [
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
    ('analyst', 'Data Analyst'),
]

SPECIALIZATION_CHOICES = [
    # Core Medical
    ('general_medicine', 'General Medicine'),
    ('cardiology', 'Cardiology'),
    ('neurology', 'Neurology'),
    ('orthopedics', 'Orthopedics'),
    ('dermatology', 'Dermatology'),
    ('psychiatry', 'Psychiatry'),
    ('pediatrics', 'Pediatrics'),
    ('gynecology', 'Gynecology'),
    ('obstetrics', 'Obstetrics'),

    # Surgery
    ('general_surgery', 'General Surgery'),
    ('neurosurgery', 'Neurosurgery'),
    ('cardiac_surgery', 'Cardiac Surgery'),
    ('plastic_surgery', 'Plastic Surgery'),
    ('urology', 'Urology'),

    # Diagnostics & Internal
    ('endocrinology', 'Endocrinology'),
    ('gastroenterology', 'Gastroenterology'),
    ('pulmonology', 'Pulmonology'),
    ('nephrology', 'Nephrology'),
    ('rheumatology', 'Rheumatology'),
    ('hematology', 'Hematology'),
    ('oncology', 'Oncology'),

    # Eye / ENT / Dental
    ('ophthalmology', 'Ophthalmology'),
    ('ent', 'ENT (Ear, Nose & Throat)'),
    ('dentistry', 'Dentistry'),

    # Mental & Rehab
    ('psychology', 'Psychology'),
    ('physiotherapy', 'Physiotherapy'),
    ('rehabilitation', 'Rehabilitation Medicine'),

    # Emergency & Critical Care
    ('emergency_medicine', 'Emergency Medicine'),
    ('critical_care', 'Critical Care'),

    # Women / Children
    ('fertility_specialist', 'Fertility Specialist'),
    ('neonatology', 'Neonatology'),

    # Public Health / Others
    ('public_health', 'Public Health'),
    ('occupational_health', 'Occupational Health'),
    ('sports_medicine', 'Sports Medicine'),
]
