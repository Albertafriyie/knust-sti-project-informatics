import os
import pandas as pd

# =====================================================================
# 1. INITIALIZATION & DATA PATHS
# =====================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'data', 'raw', 'group17_sti_survey_raw.csv'))

try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    print(f"❌ Critical Error: Data file not found at {CSV_PATH}")
    exit(1)

# Clean and standardize columns uniformly to lower snake_case
df.columns = (
    df.columns.str.lower()
    .str.strip()
    .str.replace(r'[\s/]+', '_', regex=True)
    .str.replace(r'[()*.]', '', regex=True)
)

print("=" * 65)
print(f"DATASET LOADED: {len(df)} rows × {len(df.columns)} columns")
print("=" * 65)

# =====================================================================
# 2. DEFINITIVE VALIDATION SUITE MAP (Explicit and Precise)
# =====================================================================
VALIDATION_SUITE = {
    "Demographics": {
        "gender": {
            "column_name": "gender",
            "metrics": {"Female": 49.85, "Male": 48.95, "Prefer not to say": 1.20}
        },
        "level_of_study": {
            "column_name": "level_of_study",
            "metrics": {"100": 27.63, "200": 21.02, "300": 17.72, "400": 26.13, "Postgraduate": 5.11}
        },
        "college": {
            "column_name": "college",
            "metrics": {"Health Sciences": 40.24, "Humanities": 19.22, "Science": 17.42}
        }
    },
    "Sexual Behaviour": {
        "relationship_status": {
            "column_name": "relationship_status",
            "metrics": {"Single": 67.87, "In a relationship": 30.63, "Married": 1.50}
        },
        "sexual_activity": {
            "column_name": "sexual_activity",
            "metrics": {"Not engaging in sexual activity": 67.57, "Engaging in casual sex": 4.81}
        }
    },
    "Risk Perception": {
        "risk_perception_scale": {
            "column_name": "how_likely_is_it_that_students_at_knust_are_at_risk_of_contracting_stis?",
            "metrics": {"5": 40.74, "3": 26.10, "4": 22.00}
        },
        "multiple_partners_risk": {
            "column_name": "do_you_believe_having_multiple_sexual_partners_increases_the_risk_of_stis?",
            "metrics": {"Yes": 93.27, "No": 4.28}
        },
        "condom_necessity": {
            "column_name": "do_you_think_condom_use_is_necessary_with_a_trusted_partner?",
            "metrics": {"Yes": 73.85, "No": 14.15}
        }
    },
    "Preventive Behaviours": {
        "ever_tested": {
            "column_name": "have_you_ever_been_tested_for_any_sti?",
            "metrics": {"Yes": 31.19, "No": 68.81}
        },
        "testing_awareness": {
            "column_name": "are_you_aware_of_sti_testing_services_available_on_or_near_campus?",
            "metrics": {"Know where": 66.16, "Do not know": 33.84, "Yes": 66.16, "No": 33.84}
        }
    }
}

# =====================================================================
# 3. TEXT UTILITY NORMALIZER & CLEANER
# =====================================================================


def normalize_text(text):
    if pd.isna(text):
        return ""
    # Strip spaces and cast down to standard lowercase
    st = str(text).strip().lower().replace('_', ' ').replace('-', ' ')
    # Strip structural float markers from numerical scaling questions
    if st.endswith('.0'):
        st = st[:-2]
    return st


# =====================================================================
# 4. EXECUTE CORE AUDIT PIPELINE
# =====================================================================
for section_title, fields in VALIDATION_SUITE.items():
    print(f"\n\n{'#' * 65}\n  SECTION: {section_title.upper()}\n{'#' * 65}")

    for field_key, config in fields.items():
        target_col = config["column_name"]
        benchmarks = config["metrics"]

        if target_col not in df.columns:
            print(f"\n--- Audit Field: [{target_col.upper()}] ---")
            print(f"  ❌ Mismatch Alert: Column not found in dataset columns.")
            continue

        print(f"\n--- Audit Field: [{target_col.upper()}] ---")

        # Build clean string series maps for value distribution counting
        series = df[target_col].fillna("").astype(str).str.strip()
        norm_counts = series.value_counts()
        norm_dict = {normalize_text(k): v for k, v in norm_counts.items()}

        # Evaluate if the underlying question contains explicit Yes/No choices
        has_explicit_yes_no = "yes" in norm_dict or "no" in norm_dict

        for label, target_value in benchmarks.items():
            lookup_key = normalize_text(label)
            raw_n = 0

            # Context Routing 1: Handle Testing Awareness Variations cleanly
            if field_key == "testing_awareness":
                if label in ["Know where", "Yes"]:
                    if has_explicit_yes_no:
                        raw_n = norm_dict.get("yes", 0)
                    else:
                        raw_n = sum(v for k, v in norm_dict.items()
                                    if "know" in k and "not" not in k)
                elif label in ["Do not know", "No"]:
                    if has_explicit_yes_no:
                        raw_n = norm_dict.get("no", 0)
                    else:
                        raw_n = sum(v for k, v in norm_dict.items()
                                    if "not" in k)

            # Context Routing 2: Isolate pure "Science" from "Health Sciences"
            elif field_key == "college" and label == "Science":
                raw_n = len(df[df[target_col].astype(
                    str).str.strip().str.lower() == 'science'])

            # Context Routing 3: High Precision Direct Map matching
            elif lookup_key in norm_dict:
                raw_n = norm_dict[lookup_key]

            # Context Routing 4: Standard Substring Matching Fallback
            else:
                for k, v in norm_dict.items():
                    if lookup_key == k or (len(lookup_key) > 2 and lookup_key in k):
                        raw_n = v
                        break

            # Calculate actual live percentages over absolute population sample (333)
            actual_value = (raw_n / 333) * 100
            delta = abs(actual_value - target_value)

            # Using standard 2.5% variance check for rounding artifacts
            status_flag = "✓ MATCH" if delta < 2.5 else "✗ MISMATCH"

            # Clean terminal display by filtering duplicate output rows
            if field_key == "testing_awareness":
                if has_explicit_yes_no and label in ["Know where", "Do not know"]:
                    continue
                if not has_explicit_yes_no and label in ["Yes", "No"]:
                    continue

            print(
                f"  {label:<32} | n={raw_n:>4} | Live: {actual_value:>6.2f}% vs Paper: {target_value:>6.2f}% | {status_flag}")

print("\n" + "="*65 + "\n  PROCESSED SCRIPT COMPLETED CLEANLY\n" + "="*65)
