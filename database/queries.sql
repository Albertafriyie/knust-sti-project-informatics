-- ====================================================================
-- ADVANCED CLINICAL HEALTH INFORMATICS BI-STATISTICAL QUERIES
-- DEMONSTRATING COMPLIANCE WITH ADVANCED EHR REVENUE/METRIC REPORTING
-- ====================================================================

-- 📊 QUERY 1: MULTI-TABLE JOIN & STRATIFIED PREVALENCE AGGREGATION
-- Target: Calculate total cohort size, average age, clinic awareness rate,
-- and absolute screening prevalence stratified by Institutional College.

SELECT 
    ap.college AS institutional_college,
    COUNT(p.patient_id) AS total_monitored_cohort,
    ROUND(AVG(p.age), 1) AS average_patient_age,
    ROUND(
        SUM(CASE WHEN sr.aware_testing_services = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.patient_id), 
        1
    ) AS clinic_awareness_percentage,
    ROUND(
        SUM(CASE WHEN sr.ever_tested = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(p.patient_id), 
        1
    ) AS screening_prevalence_percentage
FROM patients p
INNER JOIN academic_profiles ap ON p.patient_id = ap.patient_id
INNER JOIN survey_responses sr ON p.patient_id = sr.patient_id
GROUP BY ap.college
ORDER BY screening_prevalence_percentage DESC;


-- 📈 QUERY 2: ADVANCED WINDOW FUNCTIONING & RISK-INSULATION RANKING
-- Target: Compute the average peer risk perception exclusively for partnered 
-- individuals, and rank colleges to isolate where risk blindness peaks.

WITH PartneredRiskCohort AS (
    SELECT 
        ap.college,
        sr.peer_risk_perception,
        sr.relationship_status,
        AVG(sr.peer_risk_perception) OVER(PARTITION BY ap.college) AS college_avg_peer_risk
    FROM survey_responses sr
    INNER JOIN academic_profiles ap ON sr.patient_id = ap.patient_id
    WHERE sr.relationship_status IN ('In a relationship', 'Married')
)
SELECT 
    college,
    ROUND(college_avg_peer_risk, 2) AS partnered_mean_risk_perception,
    RANK() OVER (ORDER BY college_avg_peer_risk ASC) AS risk_blindness_priority_rank
FROM PartneredRiskCohort
GROUP BY college
ORDER BY risk_blindness_priority_rank ASC;