import os
import re
import pandas as pd

# ──────────────────────────────────────────────────────────────────────
# 0. CONFIGURATION & CONSTANTS
# ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'data', 'raw', 'group17_sti_survey_raw.csv'))
CLEAN_PATH = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'data', 'processed', 'group17_clean.csv'))

EXPECTED_ROWS = 333

RENAME_MAP = {
    # Demographics
    "your_current_relationship_status": "relationship_status",
    "what_is_your_current_sexual_activity_status": "sexual_activity_status",
    "how_many_sexual_partners_have_you_had_in_the_past_2_years": "partners_last_2yrs",
    "what_is_the_total_number_of_lifetime_sexual_partners": "lifetime_partners",
    # Risk Perception
    "do_you_consider_yourself_at_risk_of_contracting_an_sti": "self_perceived_risk",
    "how_concerned_are_you_about_stis": "concern_level",
    "do_you_believe_having_multiple_sexual_partners_increases_the_risk_of_stis": "believes_multiple_partners_risk",
    "do_you_think_condom_use_is_necessary_with_a_trusted_partner": "condom_with_trusted_partner",
    # Preventive Behaviours
    "do_you_consistently_use_condoms_during_sexual_intercourse": "condom_use_consistency",
    "have_you_ever_been_tested_for_any_sti": "ever_tested_sti",
    "have_you_ever_tested_positive_for_any_sti": "tested_positive_sti",
    "are_you_aware_of_sti_testing_services_available_on_or_near_campus": "aware_testing_services",
    "would_you_inform_a_sexual_partner_if_you_were_diagnosed_with_an_sti": "willing_to_disclose",
}

STR_RESPONSE_COLS = [
    'gender', 'relationship_status', 'sexual_activity_status', 'self_perceived_risk',
    'believes_multiple_partners_risk', 'condom_with_trusted_partner', 'condom_use_consistency',
    'ever_tested_sti', 'tested_positive_sti', 'aware_testing_services', 'willing_to_disclose'
]

NUMERIC_TYPES = {
    col: 'Int64' for col in ['age', 'level_of_study', 'concern_level', 'partners_last_2yrs', 'lifetime_partners']
}

# ──────────────────────────────────────────────────────────────────────
# 1. CORE PIPELINE FUNCTIONS
# ──────────────────────────────────────────────────────────────────────


def load_data(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"❌ Critical Error: Data file not found at {path}")
        exit(1)


def standardise_column_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans up special characters and replaces spaces/slashes with underscores."""
    df = df.copy()
    # Batch-strip symbols and handle spacing delimiters via regex vectorization
    clean_headers = (
        df.columns.str.lower().str.strip()
        .str.replace(r"[()\*.\?,'\"]", "", regex=True)
        .str.replace(r"[ /]", "_", regex=True)
    )
    # Deduplicate sequential underscores and strip trailing edge underscores
    df.columns = [re.sub(r'_+', '_', c).strip('_') for c in clean_headers]
    return df


def filter_consent(df: pd.DataFrame) -> pd.DataFrame:
    """Finds the consent column dynamically and retains only explicit 'Yes' entries."""
    df = df.copy()
    consent_cols = [c for c in df.columns if 'consent' in c]
    if consent_cols:
        col = consent_cols[0]
        df[col] = df[col].astype(str).str.strip().str.title()
        df = df[df[col] == 'Yes']
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates all domain-specific derived analytical columns cleanly."""
    df = df.copy()

    if 'age' in df.columns:
        df['age_group'] = pd.cut(df['age'], bins=[17, 20, 24, 200], labels=[
                                 '≤20', '21–24', '≥25'])
        df['age_binary'] = (df['age'] >= 21).astype('Int64')

    if 'sexual_activity_status' in df.columns:
        df['sexually_active'] = ~df['sexual_activity_status'].astype(
            str).str.contains('Not engaging')

    if 'self_perceived_risk' in df.columns:
        df['risk_numeric'] = df['self_perceived_risk'].map(
            {'Yes': 1.0, 'No': 0.0, 'Maybe': 0.5})

    if all(c in df.columns for c in ['sexually_active', 'believes_multiple_partners_risk', 'self_perceived_risk']):
        df['knowledge_practice_gap'] = (df['sexually_active']) & \
                                       (df['believes_multiple_partners_risk'] == 'Yes') & \
                                       (df['self_perceived_risk'] == 'No')

    if 'condom_use_consistency' in df.columns:
        condom_map = {'Always': 'Low Risk', 'Sometimes': 'Moderate Risk',
                      'Never': 'High Risk', 'Not Sexually Active': 'Not Applicable'}
        df['condom_risk_level'] = df['condom_use_consistency'].map(condom_map)

    return df

# ──────────────────────────────────────────────────────────────────────
# 2. EXECUTIVE EXECUTION FLOW
# ──────────────────────────────────────────────────────────────────────


def run_pipeline():
    print("=" * 65 + "\nRUNNING REFACTORED PRODUCTION PIPELINE\n" + "=" * 65)

    # Load & Initial Validation Checks
    raw_df = load_data(RAW_PATH)
    print(
        f"Step 0: Data Loaded. Shape: {raw_df.shape[0]} rows × {raw_df.shape[1]} cols")
    if raw_df.shape[0] != EXPECTED_ROWS:
        print(
            f"  ⚠ Delta Check: Row count deviates by {raw_df.shape[0] - EXPECTED_ROWS:+d} rows.")

    # Structural Formatting & Renaming
    df = standardise_column_headers(raw_df)
    df = df.rename(
        columns={k: v for k, v in RENAME_MAP.items() if k in df.columns})

    # Deduplication & Consent Filtering
    before_drop = len(df)
    df = df.drop_duplicates()
    df = filter_consent(df)
    print(
        f"Step 1: Dedup & Consent Filter applied. Dropped {before_drop - len(df)} row(s).")

    # Data Categorization Cleanups (Title-casing)
    for col in STR_RESPONSE_COLS:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip().str.title()

    # Sweep remaining non-categorical text strings to cleanly strip whitespaces
    # and support explicit string types forward-compatibly (silencing Pandas4Warning)
    other_str_cols = df.select_dtypes(
        include=['object', 'string']).columns.difference(STR_RESPONSE_COLS)
    df[other_str_cols] = df[other_str_cols].apply(
        lambda s: s.astype(str).str.strip())

    # Type Corrections safely utilizing to_numeric coercion
    for col, dtype in NUMERIC_TYPES.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(dtype)

    # Feature Engineering
    df = engineer_features(df)
    print(
        f"Step 2: Feature Engineering complete. Final Shape: {df.shape[0]} rows × {df.shape[1]} cols")

    # Dynamic File Tree Operations: Build missing directories right before saving
    output_dir = os.path.dirname(CLEAN_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"  → Created missing directory tree structure: {output_dir}")

    # File Persistence & Integrity Validation
    df.to_csv(CLEAN_PATH, index=False)
    verify_df = pd.read_csv(CLEAN_PATH)
    assert len(df) == len(
        verify_df), "CRITICAL ERROR: Export Row Count Mismatch!"
    print(
        f"Step 3: Clean file saved successfully to:\n         '{CLEAN_PATH}'\n" + "=" * 65)


if __name__ == "__main__":
    run_pipeline()
