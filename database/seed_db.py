import os
import sqlite3
import pandas as pd

# 1. Establish absolute directory path tracking to prevent terminal execution errors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "knust_health.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
RAW_DATA_PATH = os.path.normpath(os.path.join(
    BASE_DIR, "..", "data", "group17_clean.csv"))

print("🚀 Initializing EHR Relational Database Seeding Engine...")

# 2. Establish connection to the local database file
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 3. Read and execute the structural schema.sql script
if not os.path.exists(SCHEMA_PATH):
    raise FileNotFoundError(
        f"❌ ERROR: Missing structural schema file at: {SCHEMA_PATH}\nMake sure schema.sql is placed in the database/ folder!")

with open(SCHEMA_PATH, "r") as f:
    schema_sql = f.read()
cursor.executescript(schema_sql)
conn.commit()
print("📁 SUCCESS: 3rd Normal Form tables and optimization indices created successfully.")

# 4. Ingest raw cohort matrix using Pandas for parsing
if not os.path.exists(RAW_DATA_PATH):
    raise FileNotFoundError(
        f"❌ ERROR: Missing raw survey file at: {RAW_DATA_PATH}\nMake sure group17_clean.csv is placed in the data/ folder!")

df = pd.read_csv(RAW_DATA_PATH)

# Dynamic string column mapping to safeguard against file variations
gender_col = [col for col in df.columns if 'gender' in col.lower()
              or 'sex' in col.lower()][0]
risk_col = [col for col in df.columns if 'risk_of_contracting' in col.lower(
) or 'likely_is_it' in col.lower()][0]
rel_col = [col for col in df.columns if 'relationship' in col.lower()
           or 'status' in col.lower()][0]
aware_col = [col for col in df.columns if 'aware' in col.lower()
             and 'testing' in col.lower()][0]
target_col = [col for col in df.columns if 'ever_tested' in col.lower() or (
    'ever' in col.lower() and 'test' in col.lower())][0]

print(f"📦 Processing {len(df)} survey rows for database streaming...")

# 5. Seed the relational tables
for row_idx, (_, row) in enumerate(df.iterrows(), start=1):
    patient_id = f"KNUST-2026-PID{row_idx:04d}"
    age_val = int(row['age']) if pd.notnull(row['age']) else 22

    # Seed Table 1: Patients
    cursor.execute(
        "INSERT INTO patients (patient_id, age, gender) VALUES (?, ?, ?)",
        (patient_id, age_val, str(row[gender_col]).strip())
    )

    # Seed Table 2: Academic Profiles
    cursor.execute(
        "INSERT INTO academic_profiles (patient_id, college) VALUES (?, ?)",
        (patient_id, str(row['college']).strip())
    )

    # Seed Table 3: Survey Responses
    cursor.execute(
        """INSERT INTO survey_responses 
           (patient_id, aware_testing_services, peer_risk_perception, relationship_status, ever_tested) 
           VALUES (?, ?, ?, ?, ?)""",
        (
            patient_id,
            str(row[aware_col]).strip(),
            int(row[risk_col]) if pd.notnull(row[risk_col]) else 3,
            str(row[rel_col]).strip(),
            str(row[target_col]).strip()
        )
    )

# Commit transactions and secure data locks
conn.commit()

# Verify structural ingestion integrity
patient_count = cursor.execute("SELECT COUNT(*) FROM patients;").fetchone()[0]
print(
    f"🎯 DATABASE SEEDED PERFECTLY: {patient_count} patient records verified inside SQL relational storage!")

conn.close()
