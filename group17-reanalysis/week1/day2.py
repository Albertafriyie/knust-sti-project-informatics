# ===
# Part A - The Dictionary
# One respondent, all fields in one container
# Compare to Day 1 where these were 30 separate variables
# ===

respondent_sti_001 = {
    # Section A — Demographics
    "id":                    "STI-001",
    "age":                   21,
    "gender":                "Female",
    "college":               "Health Sciences",
    "level_of_study":        200,
    "relationship_status":   "Single",
    "sexual_activity":       "Not engaging in sexual activity",
    "partners_last_2yrs":    0,
    "lifetime_partners":     0,

    # Section B — STI Awareness (True = heard of this STI)
    "aware_hiv":             True,    # 99.4% in Figure 5.4.1
    "aware_syphilis":        True,    # 93.9%
    "aware_gonorrhoea":      True,    # 93.3%
    "aware_hepatitis_b":     True,    # 88.4%
    "aware_chlamydia":       True,    # 73.9%
    "aware_herpes":          True,    # 70.5%
    "aware_hpv":             False,   # 57.4% — notable gap
    "aware_trichomoniasis":  False,   # 47.4% — lowest

    # Section B — Transmission knowledge
    # False here = INCORRECT answer given (mirrors Tables 5.5.1–5.5.4)
    # Only 26.06% correct (Table 5.5.3)
    "correct_hiv_not_kissing":         False,
    # 68.73% got this WRONG (Table 5.5.1)
    "correct_syphilis_not_razor":      False,
    # 47.08% got this WRONG (Table 5.5.1)
    "correct_syphilis_not_toilet":     False,
    # 47.55% got this WRONG (Table 5.5.2)
    "correct_chlamydia_not_toilet":    False,
    # Only 42.68% correct (Table 5.5.2)
    "correct_chlamydia_vertical_trans": False,

    # Section C — Risk perception
    "self_perceived_risk":   "No",    # 70.25% said No (Figure 5.6.1)
    "concern_level":         4,       # 65.03% rated 4 or 5 (Table 5.6.1)
    "believes_multi_partner_risk": True,  # 93.27% said Yes (Table 5.6.1)
    "believes_condom_trusted":     True,  # 73.85% said Yes (Table 5.6.1)

    # Section D — Preventive behaviors
    "condom_use_consistency": "Not sexually active",  # 56.92% (Table 5.7.1)
    "ever_tested_sti":        False,  # 68.81% never tested (Table 5.7.1)
    "tested_positive":        False,
    "aware_testing_services": True,   # 66.16% know where (Figure 5.4.2)
    "willing_to_disclose":    "Yes",  # 77.85% said Yes (Table 5.7.1)
}

# ===
# Part B — Accessing Values From a Dictionary
# This is what Pandas does when df["column_name"] is typed
# ===

# Accessing individual fields
print(f"Respondent ID:     {respondent_sti_001['id']}")
print(f"Age:               {respondent_sti_001['age']}")
print(f"College:           {respondent_sti_001['college']}")
print(f"Self-risk:         {respondent_sti_001['self_perceived_risk']}")
print(f"Ever tested:       {respondent_sti_001['ever_tested_sti']}")

# Build a formatted summary (like printing one row of STATA output)
print("\n--- Respondent Summary ---")
print(f"{respondent_sti_001['id']} | "
      f"{respondent_sti_001['gender']}, "
      f"Age {respondent_sti_001['age']} | "
      f"{respondent_sti_001['college']} | "
      f"Level {respondent_sti_001['level_of_study']}")

# Check the knowledge-practice gap for this respondent
# (The core finding of Chapter 6.4)
knows_risk = respondent_sti_001["believes_multi_partner_risk"]
self_risk = respondent_sti_001["self_perceived_risk"]
is_active = respondent_sti_001["sexual_activity"] != "Not engaging in sexual activity"

print(f"\nKnowledge-practice gap check:")
print(f"  Believes multiple partners = risk: {knows_risk}")
print(f"  Personally feels at risk:          {self_risk}")
print(f"  Currently sexually active:         {is_active}")

if knows_risk == True and self_risk == "No":
    print("  --> OPTIMISTIC BIAS: knows risk, denies personal vulnerability")
    print("  --> This respondent is in the 93.27% who know (Table 5.6.1)")
    print("     but in the 70.25% who deny personal risk (Figure 5.6.1)")

# ===
# Part C — Adding Derived Variables to a Dictionary
# ===

# Count how many transmission questions this respondent got wrong
incorrect_transmission = [
    key for key, val in respondent_sti_001.items()
    if key.startswith("correct_") and val == False
]

misconception_count = len(incorrect_transmission)
respondent_sti_001["misconception_count"] = misconception_count
respondent_sti_001["has_toilet_myth"] = (
    respondent_sti_001["correct_syphilis_not_toilet"] == False or
    respondent_sti_001["correct_chlamydia_not_toilet"] == False
)

print(f"\nDerived variables added:")
print(f"  Misconceptions: {misconception_count} out of 5 checked")
print(f"  Topics: {incorrect_transmission}")
print(f"  Toilet seat myth holder: {respondent_sti_001['has_toilet_myth']}")
print(f"  (Your paper: 57.8% for gonorrhoea, 47.08–47.55% for syphilis/chlamydia)")

# Count STI awareness score
aware_keys = [k for k in respondent_sti_001 if k.startswith("aware_")]
aware_count = sum(1 for k in aware_keys if respondent_sti_001[k] == True)
aware_total = len(aware_keys)
awareness_pct = (aware_count / aware_total) * 100
respondent_sti_001["awareness_score_pct"] = round(awareness_pct, 1)
print(
    f"  STI awareness score: {aware_count}/{aware_total} = {awareness_pct:.1f}%")


# ===
# Part D — The List
# Multiple respondents in one collection
# This is structurally identical to STATA dataset
# Each dictionary here = one row in CSV
# ===

# Ten respondents reflecting the actual demographic spread in study:
# College of Health Sciences = 40.24% → 4 of 10
# Humanities = 19.22% → 2 of 10
# Science = 17.42% → 2 of 10
# Engineering = 9.91% → 1 of 10
# Agriculture = 5.71% → 1 of 10
# Arts = 7.51% → (combined with Science here for simplicity)
#
# Gender: ~50/50 female/male → 5 of each
# Level: L100=27.63%, L200=21.02%, L300=17.72%, L400=26.13%
#   → 3 L100, 2 L200, 2 L300, 3 L400
# Sexual activity: 67.57% not active → 7 of 10 not active
# Self-perceived risk No = 70.25% → 7 of 10

cohort = [
    # Respondent 1 — Health Sciences, Female, Level 200, not active
    {
        "id": "STI-001", "age": 21, "gender": "Female",
        "college": "Health Sciences", "level": 200,
        "sexual_active": False,
        "self_perceived_risk": "No",
        "condom_use": "Not sexually active",
        "ever_tested": False,
        "aware_hpv": False,             # 57.4% unaware in your study
        "aware_trichomoniasis": False,   # 47.4% unaware
        # 47–57% held this (Tables 5.5.1–5.5.4)
        "toilet_seat_myth": True,
        "knowledge_score": 16,
        "concern_level": 4
    },
    # Respondent 2 — Humanities, Male, Level 400, sexually active
    {
        "id": "STI-002", "age": 22, "gender": "Male",
        "college": "Humanities", "level": 400,
        "sexual_active": True,
        "self_perceived_risk": "Yes",
        "condom_use": "Sometimes",
        "ever_tested": False,
        "aware_hpv": False,
        "aware_trichomoniasis": False,
        "toilet_seat_myth": True,
        "knowledge_score": 11,
        "concern_level": 3
    },
    # Respondent 3 — Science, Female, Level 100, not active
    {
        "id": "STI-003", "age": 20, "gender": "Female",
        "college": "Science", "level": 100,
        "sexual_active": False,
        "self_perceived_risk": "No",
        "condom_use": "Not sexually active",
        "ever_tested": False,
        "aware_hpv": True,
        "aware_trichomoniasis": False,
        "toilet_seat_myth": False,
        "knowledge_score": 14,
        "concern_level": 4
    },
    # Respondent 4 — Engineering, Male, Level 400, casual sex
    # Reflects your Table 5.8.4: casual sex → 56.25% perceive themselves at risk
    {
        "id": "STI-004", "age": 23, "gender": "Male",
        "college": "Engineering", "level": 400,
        "sexual_active": True,
        "self_perceived_risk": "Yes",
        "condom_use": "Never",
        "ever_tested": True,
        "aware_hpv": False,
        "aware_trichomoniasis": False,
        "toilet_seat_myth": True,
        "knowledge_score": 9,
        "concern_level": 2
    },
    # Respondent 5 — Health Sciences, Female, Level 100, not active
    {
        "id": "STI-005", "age": 19, "gender": "Female",
        "college": "Health Sciences", "level": 100,
        "sexual_active": False,
        "self_perceived_risk": "No",
        "condom_use": "Not sexually active",
        "ever_tested": False,
        "aware_hpv": True,
        "aware_trichomoniasis": True,
        "toilet_seat_myth": False,
        "knowledge_score": 17,
        "concern_level": 5
    },
    # Respondent 6 — Humanities, Male, Level 400, committed not married
    {
        "id": "STI-006", "age": 24, "gender": "Male",
        "college": "Humanities", "level": 400,
        "sexual_active": True,
        "self_perceived_risk": "No",
        "condom_use": "Sometimes",
        "ever_tested": False,
        "aware_hpv": False,
        "aware_trichomoniasis": False,
        "toilet_seat_myth": True,
        "knowledge_score": 8,
        "concern_level": 3
    },
    # Respondent 7 — Science, Female, Level 300, committed not married
    # Reflects Table 5.8.4: committed non-married → 22.89% at risk
    {
        "id": "STI-007", "age": 21, "gender": "Female",
        "college": "Science", "level": 300,
        "sexual_active": True,
        "self_perceived_risk": "No",
        "condom_use": "Always",
        "ever_tested": True,
        "aware_hpv": True,
        "aware_trichomoniasis": False,
        "toilet_seat_myth": False,
        "knowledge_score": 15,
        "concern_level": 4
    },
    # Respondent 8 — Health Sciences, Male, Level 200, not active
    {
        "id": "STI-008", "age": 22, "gender": "Male",
        "college": "Health Sciences", "level": 200,
        "sexual_active": False,
        "self_perceived_risk": "No",
        "condom_use": "Not sexually active",
        "ever_tested": False,
        "aware_hpv": False,
        "aware_trichomoniasis": False,
        "toilet_seat_myth": True,
        "knowledge_score": 13,
        "concern_level": 3
    },
    # Respondent 9 — Agriculture, Female, Level 100, not active
    {
        "id": "STI-009", "age": 18, "gender": "Female",
        "college": "Agriculture", "level": 100,
        "sexual_active": False,
        "self_perceived_risk": "Maybe",
        "condom_use": "Not sexually active",
        "ever_tested": False,
        "aware_hpv": False,
        "aware_trichomoniasis": False,
        "toilet_seat_myth": True,
        "knowledge_score": 10,
        "concern_level": 4
    },
    # Respondent 10 — Health Sciences, Male, Level 300, not active
    {
        "id": "STI-010", "age": 22, "gender": "Male",
        "college": "Health Sciences", "level": 300,
        "sexual_active": False,
        "self_perceived_risk": "No",
        "condom_use": "Not sexually active",
        "ever_tested": False,
        "aware_hpv": True,
        "aware_trichomoniasis": False,
        "toilet_seat_myth": False,
        "knowledge_score": 12,
        "concern_level": 3
    },
]


# ===
# Part E — Basic List Operations
# These are identical to what STATA does with describe/tabulate
# ===

# Count respondents
n = len(cohort)
print(f"\n=== COHORT OVERVIEW ===")
print(f"Total respondents: {n} (your full study has 333)")

# Access specific respondents
print(
    f"\nFirst respondent:  {cohort[0]['id']} | {cohort[0]['gender']} | {cohort[0]['college']}")
print(
    f"Last respondent:   {cohort[-1]['id']} | {cohort[-1]['gender']} | {cohort[-1]['college']}")
print(
    f"Third respondent:  {cohort[2]['id']} | {cohort[2]['gender']} | {cohort[2]['college']}")

# List slicing — first 5 respondents (like opening the first page of STATA data viewer)
first_five = cohort[:5]
print(f"\nFirst 5 respondent IDs: {[r['id'] for r in first_five]}")

# All female respondents
females = [r for r in cohort if r["gender"] == "Female"]
males = [r for r in cohort if r["gender"] == "Male"]
print(f"\nGender split: {len(females)} female, {len(males)} male")
print(f"Expected from your Table 5.2.1: 49.85% female, 48.95% male")


# PART F — LOOPING THROUGH THE COHORT
# This is what Pandas does internally when you call df.apply()
# Understanding this loop makes Day 5 groupby() feel obvious
# ====

print("\n=== RESPONDENT-BY-RESPONDENT REVIEW ===")
print(f"{'ID':<10} {'Gender':<8} {'College':<20} {'Risk':<8} {'Score':>6}")
print("-" * 60)

for respondent in cohort:
    print(
        f"{respondent['id']:<10} "
        f"{respondent['gender']:<8} "
        f"{respondent['college']:<20} "
        f"{respondent['self_perceived_risk']:<8} "
        f"{respondent['knowledge_score']:>6}/20"
    )


# ===
# Part G — Manual Frequency Counts
# Reproduce Figure 5.6.1 (self-perceived risk) and
# Table 5.7.1 (preventive behaviors) for your 10-person cohort
# Compare results to your paper's published percentages
# ===

print("\n=== SELF-PERCEIVED RISK (Figure 5.6.1) ===")
risk_yes = sum(1 for r in cohort if r["self_perceived_risk"] == "Yes")
risk_no = sum(1 for r in cohort if r["self_perceived_risk"] == "No")
risk_maybe = sum(1 for r in cohort if r["self_perceived_risk"] == "Maybe")

print(f"  Yes:   n={risk_yes}  ({risk_yes/n*100:.1f}%)  | Paper: 19.33%")
print(f"  No:    n={risk_no}  ({risk_no/n*100:.1f}%)  | Paper: 70.25%")
print(f"  Maybe: n={risk_maybe}  ({risk_maybe/n*100:.1f}%)  | Paper: 10.43%")
print(f"  (Your mock cohort of 10 will not match exactly — that is expected)")

print("\n=== CONDOM USE (Figure 5.7.1 — sexually active only) ===")
sexually_active = [r for r in cohort if r["sexual_active"] == True]
n_active = len(sexually_active)
print(f"  Sexually active in this cohort: {n_active}")

if n_active > 0:
    always = sum(1 for r in sexually_active if r["condom_use"] == "Always")
    sometimes = sum(
        1 for r in sexually_active if r["condom_use"] == "Sometimes")
    never = sum(1 for r in sexually_active if r["condom_use"] == "Never")
    print(
        f"  Always:    {always} ({always/n_active*100:.1f}%)  | Paper: 27.9%")
    print(
        f"  Sometimes: {sometimes} ({sometimes/n_active*100:.1f}%)  | Paper: 47.9%")
    print(f"  Never:     {never} ({never/n_active*100:.1f}%)  | Paper: 24.3%")

print("\n=== STI TESTING UPTAKE (Table 5.7.1) ===")
tested = sum(1 for r in cohort if r["ever_tested"] == True)
not_tested = sum(1 for r in cohort if r["ever_tested"] == False)
print(f"  Ever tested:  {tested} ({tested/n*100:.1f}%)  | Paper: 31.19%")
print(
    f"  Never tested: {not_tested} ({not_tested/n*100:.1f}%)  | Paper: 68.81%")

print("\n=== HPV AWARENESS (Figure 5.4.1) ===")
hpv_aware = sum(1 for r in cohort if r["aware_hpv"] == True)
print(f"  HPV aware: {hpv_aware} ({hpv_aware/n*100:.1f}%)  | Paper: 57.4%")

print("\n=== TOILET SEAT MYTH HOLDERS ===")
toilet_myth = sum(1 for r in cohort if r["toilet_seat_myth"] == True)
print(f"  Hold toilet seat myth: {toilet_myth} ({toilet_myth/n*100:.1f}%)")
print(f"  Paper: 57.8% for gonorrhoea, 47.08–47.55% for syphilis/chlamydia")


# ===
# Part H — Information Sources Contrast
# Reproduces your Figure 5.3.1 vs 5.3.2 finding:
# What students USE vs what they TRUST are different
# ===

# Data directly from your paper (Figure 5.3.1 + Figure 5.3.2)
# This is a dictionary of dictionaries — a common data pattern

sti_information_sources = {
    "Social media": {
        "use_pct":   88.0,   # 292 of 332 (Figure 5.3.1)
        "trust_pct": 40.3,   # 133 of 330 (Figure 5.3.2)
    },
    "Internet sources": {
        "use_pct":   68.4,   # 227 of 332
        "trust_pct": 40.3,   # 133 of 330
    },
    "TV/radio health talks": {
        "use_pct":   71.7,   # 238 of 332
        "trust_pct": 43.3,   # 143 of 330
    },
    "Healthcare professionals": {
        "use_pct":   71.4,   # 237 of 332
        "trust_pct": 78.5,   # 259 of 330  <-- highest trust
    },
    "School/university courses": {
        "use_pct":   66.0,   # 219 of 332
        "trust_pct": 49.1,   # 162 of 330
    },
    "Friends or peers": {
        "use_pct":   60.8,   # 202 of 332
        "trust_pct": 20.0,   # 66 of 330
    },
    "Parents/family": {
        "use_pct":   34.3,   # 114 of 332
        "trust_pct": 20.0,   # 66 of 330
    },
}

print("\n=== INFORMATION SOURCE TRUST vs USE GAP (Figures 5.3.1 + 5.3.2) ===")
print(f"{'Source':<30} {'Used%':>7} {'Trusted%':>9} {'Gap':>7}")
print("-" * 58)

for source, data in sti_information_sources.items():
    use = data["use_pct"]
    trust = data["trust_pct"]
    gap = use - trust
    flag = " <-- TRUST GAP" if gap > 30 else ""
    print(f"  {source:<28} {use:>6.1f}%  {trust:>7.1f}%  {gap:>+6.1f}%{flag}")

# The key finding from your Chapter 5.3:
# Social media is used by 88% but only trusted by 40.3%
# Healthcare professionals are used by 71.4% AND trusted by 78.5% — alignment
most_trusted = max(sti_information_sources,
                   key=lambda s: sti_information_sources[s]["trust_pct"])
most_used = max(sti_information_sources,
                key=lambda s: sti_information_sources[s]["use_pct"])
print(
    f"\n  Most trusted source: {most_trusted} ({sti_information_sources[most_trusted]['trust_pct']}%)")
print(
    f"  Most used source:    {most_used} ({sti_information_sources[most_used]['use_pct']}%)")

if most_trusted != most_used:
    print(f"  --> MISMATCH: students primarily use '{most_used}'")
    print(f"     but trust '{most_trusted}' most")
    print(f"     This is the core finding of your Section 5.3 discussion")


# ===
# Part I — College-by-college Analysis
# Reproduces Table 5.2.3
# ===

print("\n=== COLLEGE DISTRIBUTION (Table 5.2.3) ===")
colleges = {}
for respondent in cohort:
    c = respondent["college"]
    if c not in colleges:
        colleges[c] = 0
    colleges[c] += 1

# Sort by count, descending
sorted_colleges = sorted(colleges.items(), key=lambda x: -x[1])
for college, count in sorted_colleges:
    pct = count / n * 100
    print(f"  {college:<30} {count:>3}  ({pct:.1f}%)")

print(f"\n  Your paper (Table 5.2.3):")
print(f"  Health Sciences:          134  (40.24%)")
print(f"  Humanities & Soc Sci:      64  (19.22%)")
print(f"  Science:                   58  (17.42%)")
print(f"  Engineering:               33  ( 9.91%)")
print(f"  Arts & Built Environment:  25  ( 7.51%)")
print(f"  Agriculture:               19  ( 5.71%)")

# Mean knowledge score by college (from your 10-person cohort)
print("\n=== MEAN KNOWLEDGE SCORE BY COLLEGE ===")
college_scores = {}
for respondent in cohort:
    c = respondent["college"]
    if c not in college_scores:
        college_scores[c] = []
    college_scores[c].append(respondent["knowledge_score"])

for college, scores in sorted(college_scores.items()):
    mean_score = sum(scores) / len(scores)
    print(f"  {college:<30} mean = {mean_score:.1f}/20  (n={len(scores)})")
print(f"\n  (On Day 18 you will run a proper t-test on this difference)")
print(f"  (On Day 19 you will run chi-square tests on the full n=333)")
