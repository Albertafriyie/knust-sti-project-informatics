import os
import sqlite3
import pandas as pd

# 1. Establish absolute path tracking to locate our live DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "knust_health.db")

print("📊 Connecting to EHR Relational Backend Engine...")
conn = sqlite3.connect(DB_PATH)

# ====================================================================
# CLINICAL ADVANCED SQL QUERY 1: MULTI-TABLE JOIN & PREVALENCE STRATIFICATION
# ====================================================================
query_1 = """
SELECT 
    ap.college AS [Institutional College],
    COUNT(p.patient_id) AS [Total Cohort],
    ROUND(AVG(p.age), 1) AS [Mean Age],
    ROUND(SUM(CASE WHEN sr.aware_testing_services = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.patient_id), 1) AS [Clinic Awareness %],
    ROUND(SUM(CASE WHEN sr.ever_tested = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.patient_id), 1) AS [Screening Prevalence %]
FROM patients p
INNER JOIN academic_profiles ap ON p.patient_id = ap.patient_id
INNER JOIN survey_responses sr ON p.patient_id = sr.patient_id
GROUP BY ap.college
ORDER BY [Screening Prevalence %] DESC;
"""

print("\n========================= ANALYSIS 1: STRATIFIED PREVALENCE METRICS =========================")
df_metrics = pd.read_sql_query(query_1, conn)
print(df_metrics.to_string(index=False))

# ====================================================================
# CLINICAL ADVANCED SQL QUERY 2: WINDOW FUNCTIONS FOR RISK PERCEPTION RANKING
# ====================================================================
query_2 = """
WITH PartneredRiskCohort AS (
    SELECT 
        ap.college,
        sr.peer_risk_perception,
        AVG(sr.peer_risk_perception) OVER(PARTITION BY ap.college) AS college_avg_peer_risk
    FROM survey_responses sr
    INNER JOIN academic_profiles ap ON sr.patient_id = ap.patient_id
    WHERE sr.relationship_status IN ('In a relationship', 'Married', 'Partnered')
)
SELECT 
    college AS [Institutional College],
    ROUND(college_avg_peer_risk, 2) AS [Partnered Mean Risk Perception],
    RANK() OVER (ORDER BY college_avg_peer_risk ASC) AS [Risk Blindness Priority Rank]
FROM PartneredRiskCohort
GROUP BY college
ORDER BY [Risk Blindness Priority Rank] ASC;
"""

print("\n========================= ANALYSIS 2: ADVANCED WINDOW FUNCTION RANKING =========================")
df_window = pd.read_sql_query(query_2, conn)
print(df_window.to_string(index=False))

conn.close()
