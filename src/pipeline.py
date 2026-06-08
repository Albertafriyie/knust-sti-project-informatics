'''
Description: Production Ingestion & Cleansing Pipeline for KNUST STI Study.
Author: Afriyie Albert Dwamena
'''

import os
import pandas as pd
import numpy as np


def build_processed_cohort(input_file: str, output_file: str):
    '''
     Ingests raw survey data, executes structural contingency fixes,
     aligns binary knowledge variables, and features a tiered risk score. 
    '''
    print("Initializing Public Health Data Engineering Pipeline...")

    # Ensure raw file target exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Error: Raw dataset missing at: {input_file}")

    # Read raw survey instrument matrix
    df = pd.read_csv(input_file)

    # Create clean dictionary copy to prevent view mutation warnings
    clean_df = df.copy()

    # Handling Missing Partner Metrics
    # If a respondent is not sexually active, missing partner fields must equal 0.
    partner_features = ['partners_last_2yrs', 'lifetime_partners']
    for col in partner_features:
        # Convert to numeric, turn errors to NaN, fill empty spaces with 0
        clean_df[col] = pd.to_numeric(
            clean_df[col], errors='coerce').fillna(0).astype(int)

    # Exposure Feature
    # Create binary indicator: 1 for Health Sciences, 0 for all other tracks
    clean_df['college_clean'] = clean_df['college'].str.strip().str.upper()
    clean_df['is_health_science'] = np.where(
        clean_df['college_clean'] == 'HEALTH SCIENCES', 1, 0)

    # Target Variables
    # Standardize asymmetric responses into clean boolean arrays
    boolean_map = {
        'Yes': 1, 'No': 0, 'Maybe': 0,
        'I do not know': 0, 'I do not known': 0, 'I am not sexually active': 0
    }
    clean_df['knows_asymptomatic'] = clean_df['can_stis_be_transmitted_without_showing_symptoms'].map(
        boolean_map).fillna(0).astype(int)

    # Custom Feature Engineering
    def assign_behavioral_risk_tier(row):
        # Rule for High Behavioral Risk: Multi-partners or completely unprotected sex
        if row['condom_use_consistency'] == 'Never' or row['partners_last_2yrs'] > 1:
            return 2  # High Risk

        # Rule for Moderate Behavioral Risk: Inconsistent protective measures
        elif row['condom_use_consistency'] == 'Sometimes':
            return 1  # Moderate Risk

        # Baseline: Protected sex or non-active status
        else:
            return 0  # Low Risk

        clean_df['behavioral_risk_tier'] = clean_df.apply(
            assign_behavioral_risk_tier, axis=1)

    # Data Integrity Export
    # Drop intermediate transformation columns to keep data structure thin
    clean_df = clean_df.drop(columns=['college_clean'])

    # Save the polished clinical file
    clean_df.to_csv(output_file, index=False)

    print(f" Pipeline Completed Successfully!")
    print(
        f" Exported: {output_file} | Records: {clean_df.shape[0]} Rows x {clean_df.shape[1]} Columns\n")
    return clean_df


if __name__ == "__main__":
    # Standard relative paths based on repository design layout
    RAW_PATH = os.path.join("data", "group17_clean.csv")
    PROCESSED_PATH = os.path.join("data", "processed_cohort_data.csv")

    build_processed_cohort(RAW_PATH, PROCESSED_PATH)
