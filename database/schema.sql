-- ====================================================================
-- CAMPUS STI INFORMATICS - RELATIONAL EHR DATABASE SCHEMA (3NF)
-- SYSTEM DESIGNED FOR DETACHED COHORT MANAGEMENT & HIGH-SPEED QUERYING
-- ====================================================================

-- Drop tables if they already exist to ensure a clean deployment reset
DROP TABLE IF EXISTS survey_responses;
DROP TABLE IF EXISTS academic_profiles;
DROP TABLE IF EXISTS patients;

-- 1. Core Patient Table (Demographics & Structural Metadata)
CREATE TABLE patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    age INTEGER NOT NULL,
    gender VARCHAR(30) NOT NULL
);

-- 2. Academic Profiles Table (Institutional Faction Placement)
CREATE TABLE academic_profiles (
    patient_id VARCHAR(50) PRIMARY KEY,
    college VARCHAR(100) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- 3. Clinical Survey Responses Table (Behavioral Metrics & Screening Tracking)
CREATE TABLE survey_responses (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id VARCHAR(50) NOT NULL,
    aware_testing_services VARCHAR(10) NOT NULL,
    peer_risk_perception INTEGER NOT NULL,
    relationship_status VARCHAR(50) NOT NULL,
    ever_tested VARCHAR(10) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- 4. High-Performance Indexing Keys to Optimize Downstream Joins
CREATE INDEX idx_patients_gender ON patients(gender);
CREATE INDEX idx_academic_college ON academic_profiles(college);
CREATE INDEX idx_survey_ever_tested ON survey_responses(ever_tested);