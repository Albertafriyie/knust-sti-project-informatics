import pandas as pd
import os

# ===
# Part A - Load the dataset
# Build path relative to THIS script's location, not the working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'data', 'raw',
                        'group17_sti_survey_raw.csv')
print("Loading GROUP_17 survey data...")
df = pd.read_csv(csv_path)
print("Load complete.")

# ===
# Part B — Shape Verification
print("\n" + "=" * 60)
print("PART B — SHAPE VERIFICATION")
print("=" * 60)

rows, cols = df.shape
print(f"\nDataset dimensions: {rows} rows × {cols} columns")
print("Expected rows: 333 (Chapter 4.3 of your paper)")

if rows == 333:
    print("✓ Row count matches your published sample size")
elif rows > 333:
    print(f"⚠ MORE rows than expected: {rows - 333} extra rows")
    print("  Possible causes:")
    print("  - Test responses not deleted from Google Forms")
    print("  - Duplicate submissions from same respondent")
    print("  - Header rows included in export")
    print("  ACTION: Document in notes.md — investigate on Day 6")
elif rows < 333:
    print(f"⚠ FEWER rows than expected: {333 - rows} missing")
    print("  Possible causes:")
    print("  - Export was filtered before saving")
    print("  - Some respondents declined consent (Q1 = No)")
    print("  - Incomplete exports from STATA")
    print("  ACTION: Document in notes.md — investigate on Day 6")

print(f"\nColumn count: {cols}")
print("  Your questionnaire had 58 questions across 4 sections")
print("  Google Forms adds a Timestamp column → expect ~59+")
print("  Multi-select questions may expand to multiple columns")

# ===
# Part C — Column audit

print("\n" + "=" * 60)
print("PART C — COLUMN NAMES AUDIT")
print("=" * 60)

print(f"\nAll {len(df.columns)} column names in your dataset:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:>3}. {col}")

print("\nMap each column name to your questionnaire:")
print("  - Does each Section A question (Q2–Q9) have a column?")
print("  - Does each STI awareness item (Q10) have a column?")
print("  - Does each transmission knowledge item (Q13–31) have a column?")
print("  - Does each risk perception item (Q48–52) have a column?")
print("  - Does each preventive behavior item (Q53–57) have a column?")
print("\nACTION: If any expected column is missing, note it in notes.md")
print("        with the question number and what it should contain")

# ===
# PART D — DATA TYPES AUDIT
print("\n" + "=" * 60)
print("PART D — DATA TYPES AUDIT")
print("=" * 60)

print("\nColumn name → dtype → notes:")
for col in df.columns:
    dtype = str(df[col].dtype)
    n_unique = df[col].nunique()
    n_missing = df[col].isnull().sum()

    # Flag potential type mismatches
    flag = ""
    if "age" in col.lower() and dtype == "object":
        flag = "  ⚠ EXPECTED int64 — check for text values"
    elif "level" in col.lower() and dtype == "object":
        flag = "  ⚠ EXPECTED int64 — check for text values"
    elif "score" in col.lower() and dtype == "object":
        flag = "  ⚠ EXPECTED int64 — check for text values"
    elif "partner" in col.lower() and dtype == "object":
        flag = "  ⚠ EXPECTED int64 — check for text values"

    print(f"  {col:<45} {dtype:<10} unique={n_unique:<5} missing={n_missing}{flag}")

# ===
# PART E — INFO AND DESCRIBE
print("\n" + "=" * 60)
print("PART E — FULL INFO REPORT")
print("=" * 60)

# .info() prints directly — cannot be stored as a variable
print("\ndf.info() output:")
df.info()

# .describe() for numeric columns only
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if len(numeric_cols) > 0:
    print(f"\n" + "=" * 60)
    print("NUMERIC COLUMN SUMMARY (df.describe())")
    print("=" * 60)
    print(f"\nNumeric columns found: {numeric_cols}")
    print(df[numeric_cols].describe().round(2))

    # Check age statistics against your Figure 5.2.1
    if "age" in df.columns or any("age" in c.lower() for c in numeric_cols):
        age_col = [c for c in numeric_cols if "age" in c.lower()]
        if age_col:
            age_col = age_col[0]
            print(f"\nAge statistics:")
            print(f"  Min:  {df[age_col].min()} (expected: 18)")
            print(f"  Max:  {df[age_col].max()} (expected: 45)")
            print(
                f"  Mean: {df[age_col].mean():.1f} (expected: ~21–22 based on Figure 5.2.1)")
            print(f"  Most common: {df[age_col].mode()[0]} "
                  f"(expected: 22 with 64 respondents per Figure 5.2.1)")

# ===
# PART F — MISSING VALUES REPORT
print("\n" + "=" * 60)
print("PART F — MISSING VALUES REPORT")
print("=" * 60)

missing_counts = df.isnull().sum()
missing_pcts = (df.isnull().sum() / len(df) * 100).round(1)

# Build a clean report table
missing_report = pd.DataFrame({
    "Missing_n":   missing_counts,
    "Missing_pct": missing_pcts
})

# Split into two views: columns WITH missing and columns WITHOUT
has_missing = missing_report[missing_report["Missing_n"] > 0].sort_values(
    "Missing_n", ascending=False
)
no_missing = missing_report[missing_report["Missing_n"] == 0]

print(f"\nColumns WITH missing values: {len(has_missing)}")
if len(has_missing) > 0:
    print(has_missing.to_string())
    print("\nFor each column above:")
    print("  → Check if the missing pattern is EXPECTED or UNEXPECTED")
    print("  → Expected: sensitive questions (partner counts, testing history)")
    print("  → Unexpected: demographics, awareness questions")
    print("  → Document your interpretation in notes.md")
else:
    print("  No missing values found — check that this is expected")
    print("  Google Forms required fields would produce this result")

print(f"\nColumns with complete data: {len(no_missing)}")
print(f"Total columns: {len(df.columns)}")

# Flag any demographic columns with missing data
demographic_keywords = ["age", "gender", "college", "level", "relationship"]
print("\nDemographic column check (should all be complete):")
for col in df.columns:
    if any(kw in col.lower() for kw in demographic_keywords):
        n_miss = df[col].isnull().sum()
        status = "✓ Complete" if n_miss == 0 else f"⚠ {n_miss} missing"
        print(f"  {col:<40} {status}")


# ===
# PART G — SPOT-CHECKS AGAINST PUBLISHED VALUES
print("\n" + "=" * 60)
print("PART G — SPOT-CHECKS AGAINST YOUR PUBLISHED PAPER")
print("=" * 60)

# Helper function for the spot-check pattern


def spot_check(label, df, col_name, expected_values_dict):
    """
    Checks a column's value distribution against expected paper values.
    expected_values_dict: {value: expected_percentage}
    """
    print(f"\n  {label}")
    if col_name not in df.columns:
        # Try to find a close match
        close = [c for c in df.columns if col_name.lower() in c.lower()]
        if close:
            print(f"    Column '{col_name}' not found. Close matches: {close}")
            print(f"    Update col_name to the correct column name from Part C output")
        else:
            print(f"    ⚠ Column '{col_name}' not found in dataset")
            print(f"    Check the column names from Part C and update this call")
        return

    counts = df[col_name].value_counts()
    pcts = df[col_name].value_counts(normalize=True) * 100

    print(
        f"    {'Value':<35} {'N':>5}  {'Computed%':>10}  {'Expected%':>10}  {'Match':>8}")
    print(f"    {'─'*35}  {'─'*5}  {'─'*10}  {'─'*10}  {'─'*8}")

    for val, expected_pct in expected_values_dict.items():
        n_val = counts.get(val, 0)
        computed_pct = pcts.get(val, 0.0)
        diff = abs(computed_pct - expected_pct)

        if diff < 1.0:
            match = "✓ match"
        elif diff < 3.0:
            match = "~ close"
        else:
            match = "✗ CHECK"

        print(
            f"    {str(val):<35} {n_val:>5}  {computed_pct:>9.2f}%  {expected_pct:>9.2f}%  {match:>8}")


# ─────────────────────────────────────────────
# SPOT-CHECK 1: Gender (Table 5.2.1)
# Expected: Female=49.85%, Male=48.95%, Prefer not to say=1.2%
# ─────────────────────────────────────────────

# INSTRUCTION: Replace "gender" below with the EXACT column name
# from your Part C output above. Google Forms may have named it
# something like "3. GENDER *" or "Gender". Use the exact string.
GENDER_COL = "gender"   # ← UPDATE THIS after checking Part C output

spot_check(
    "GENDER — Table 5.2.1",
    df,
    GENDER_COL,
    {
        "Female":          49.85,
        "Male":            48.95,
        "Prefer not to say": 1.20
    }
)

# ─────────────────────────────────────────────
# SPOT-CHECK 2: College (Table 5.2.3)
# Expected: Health Sciences=40.24%, Humanities=19.22%,
#           Science=17.42%, Engineering=9.91%,
#           Arts=7.51%, Agriculture=5.71%
# ─────────────────────────────────────────────

COLLEGE_COL = "college"   # ← UPDATE THIS after checking Part C output

spot_check(
    "COLLEGE — Table 5.2.3",
    df,
    COLLEGE_COL,
    {
        "HEALTH SCIENCES":                40.24,
        "HUMANITIES AND SOCIAL SCIENCES": 19.22,
        "SCIENCE":                        17.42,
        "ENGINEERING":                     9.91,
        "ARTS AND BUILT ENVIRONMENT":      7.51,
        "AGRICULTURE AND NATURAL RESOURCES": 5.71
    }
)

# ─────────────────────────────────────────────
# SPOT-CHECK 3: Self-Perceived Risk (Figure 5.6.1)
# Expected: No=70.25%, Yes=19.33%, Maybe=10.43%
# ─────────────────────────────────────────────

RISK_COL = "self_perceived_risk"   # ← UPDATE THIS

spot_check(
    "SELF-PERCEIVED RISK — Figure 5.6.1",
    df,
    RISK_COL,
    {
        "No":    70.25,
        "Yes":   19.33,
        "Maybe": 10.43
    }
)

# ─────────────────────────────────────────────
# SPOT-CHECK 4: Condom Use Consistency (Table 5.7.1)
# Expected: Always=12.0%, Sometimes/Never=31.08%, Not active=56.92%
# ─────────────────────────────────────────────

CONDOM_COL = "condom_use_consistency"   # ← UPDATE THIS

spot_check(
    "CONDOM USE — Table 5.7.1",
    df,
    CONDOM_COL,
    {
        "Always":              12.00,
        "Sometimes":           None,    # combined with Never in Table 5.7.1
        "Never":               None,
        "Not sexually active": 56.92
    }
)

# ─────────────────────────────────────────────
# SPOT-CHECK 5: STI Testing (Table 5.7.1)
# Expected: Tested=31.19%, Never tested=68.81%
# ─────────────────────────────────────────────

TESTED_COL = "ever_tested_sti"   # ← UPDATE THIS

spot_check(
    "EVER TESTED FOR STI — Table 5.7.1",
    df,
    TESTED_COL,
    {
        "Yes": 31.19,
        "No":  68.81
    }
)


# ===
# PART H — FIRST 5 ROWS: READ LIKE A CLINICIAN
print("\n" + "=" * 60)
print("PART H — FIRST 5 RESPONDENTS (df.head())")
print("=" * 60)

# Transpose for easier reading (columns become rows)
print("\nFirst 5 respondents — transposed for readability:")
print(df.head().T.to_string())

print("\nLast 5 respondents (df.tail()):")
print(df.tail().T.to_string())

print("\nA random sample of 5 respondents (reproducible):")
print(df.sample(5, random_state=42).T.to_string())
# random_state=42 ensures same 5 rows every time you run this
# → important for reproducibility (your paper's Section 4.6 principle)


# ===
# PART H — FIRST 5 ROWS: READ LIKE A CLINICIAN
print("\n" + "=" * 60)
print("PART H — FIRST 5 RESPONDENTS (df.head())")
print("=" * 60)

# Transpose for easier reading (columns become rows)
print("\nFirst 5 respondents — transposed for readability:")
print(df.head().T.to_string())

print("\nLast 5 respondents (df.tail()):")
print(df.tail().T.to_string())

print("\nA random sample of 5 respondents (reproducible):")
print(df.sample(5, random_state=42).T.to_string())
# random_state=42 ensures same 5 rows every time you run this
# → important for reproducibility (your paper's Section 4.6 principle)


# ===
# PART I — UNIQUE VALUES AUDIT
print("\n" + "=" * 60)
print("PART I — UNIQUE VALUES IN CATEGORICAL COLUMNS")
print("=" * 60)

string_cols = df.select_dtypes(include="object").columns.tolist()
print(f"\nCategorical columns: {len(string_cols)}")

for col in string_cols:
    unique_vals = df[col].dropna().unique().tolist()
    n_unique = len(unique_vals)

    # Only print if there are a manageable number of unique values
    # (columns with many unique values are likely free-text responses)
    if n_unique <= 15:
        print(f"\n  {col} ({n_unique} unique values):")
        for val in sorted(str(v) for v in unique_vals):
            count = (df[col] == val).sum()
            print(f"    '{val}' → {count} respondents")
    else:
        print(f"\n  {col} ({n_unique} unique values) — too many to list")
        print(f"    First 5: {[str(v) for v in unique_vals[:5]]}")
        print(f"    This may be a free-text question or ID column")


# ===
# PART J — DATA QUALITY SUMMARY
print("\n" + "=" * 60)
print("PART J — DATA QUALITY SUMMARY FOR NOTES.MD")
print("=" * 60)

print(f"""
Copy the following into your notes.md under Day 4:

## Day 4 — Data Quality Report
### Date: [today]

### Dataset loaded: group17_sti_survey_raw.csv

### Row count:
  Loaded: {len(df)} rows
  Expected: 333 rows
  Difference: {len(df) - 333} rows
  Status: [ENTER: OK / INVESTIGATE]
  Reason if different: [ENTER YOUR NOTES]

### Column count:
  Loaded: {len(df.columns)} columns
  Expected: ~59+ (58 questions + timestamp)
  Status: [ENTER: OK / INVESTIGATE]

### Missing values:
  Columns with missing data: {missing_counts[missing_counts > 0].count()}
  [PASTE the Part F output table here]
  Expected missing: [list which missing columns you expected]
  Unexpected missing: [list any surprises]

### Spot-check results:
  Gender:           [MATCH / MISMATCH — paste computed vs expected %]
  College:          [MATCH / MISMATCH]
  Self-perceived risk: [MATCH / MISMATCH]
  Condom use:       [MATCH / MISMATCH]
  STI testing:      [MATCH / MISMATCH]

### Data type issues found:
  [List any columns where dtype was unexpected — see Part D]

### Unique value issues found:
  [List any columns where unexpected values appeared — see Part I]
  Example: "Female" and "female" both present in gender column

### Actions required on Day 6:
  1. [First cleaning step needed]
  2. [Second cleaning step needed]
  3. [etc.]
""")
