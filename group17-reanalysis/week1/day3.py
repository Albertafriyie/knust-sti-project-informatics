# ===
# Function 1 — classify_self_risk()
# Converts the text response to Figure 5.6.1 question
# "Do you consider yourself at risk of contracting an STI?"
# into a numeric value suitable for statistical analysis.
#
# In paper: Yes=19.33%, No=70.25%, Maybe=10.43%
# In Table 5.8.1 logistic regression: this becomes binary
# (Yes = 1, No = 0) — OR=2.2 for perceived risk used this encoding
# ===

def classify_self_risk(response):
    """
    Encodes self-perceived STI risk (Question 49) as a number.

    Parameters
    ----------
    response : str
        The raw survey response: "Yes", "No", or "Maybe"

    Returns
    -------
    float or None
        1.0 for Yes, 0.0 for No, 0.5 for Maybe, None for unrecognized input

    Study context
    -------------
    Used in your Table 5.8.1 logistic regression as the outcome variable.
    OR = 2.2 (95% CI: 1.2–4.1, p = 0.011) for perceived risk predicting
    STI testing behavior (your Table 5.8.1).
    """
    encoding = {
        "Yes":   1.0,
        "No":    0.0,
        "Maybe": 0.5
    }
    return encoding.get(response, None)


# ===
# Function 2 — classify_knowledge_level()
# Assigns a knowledge tier (Low / Moderate / High) based on
# a respondent's score on the transmission + symptom questions
# from Sections B of your questionnaire (Questions 13–35).
#
# Thresholds chosen to match the framing in your Chapter 5.5
# and the discussion in Chapter 6.3:
#   <60% correct  = Low knowledge
#   60–79% correct = Moderate knowledge
#   ≥80% correct  = High knowledge
#
# In your Table 5.8.1: STI Awareness was the predictor with
# OR = 2.5 (95% CI: 1.3–4.8, p = 0.006) — the strongest predictor
# of STI testing behavior.
# ===

def classify_knowledge_level(score, max_score=20):
    """
    Classifies a respondent's STI knowledge score into a tier.

    Parameters
    ----------
    score     : int or float
        Number of questions answered correctly (out of max_score)
    max_score : int, optional
        Total number of knowledge questions. Defaults to 20,
        which reflects the 20 transmission + symptom questions
        in Sections B of your GROUP_17 questionnaire
        (Questions 13–35, encoding Yes/No/Maybe for each route).

    Returns
    -------
    tuple : (str, float)
        Knowledge level label and percentage score
        e.g., ("Moderate", 70.0)

    Study context
    -------------
    Chapter 6.3 discussed how students showed strong surface-level
    knowledge of sexual transmission routes (>94% correct) but
    significant gaps in vertical transmission knowledge
    (42.7–51.99% correct) and symptom recognition (syphilis 68.52%).
    """
    if score is None:
        return "Unknown", None

    pct = (score / max_score) * 100

    if pct >= 80:
        return "High", round(pct, 1)
    elif pct >= 60:
        return "Moderate", round(pct, 1)
    else:
        return "Low", round(pct, 1)


# ===
# Function 3 — flag_knowledge_practice_gap()
# Detects the central contradiction described in Chapter 6.4:
# a respondent who knows that multiple sexual partners increases
# STI risk (93.27% said Yes in Table 5.6.1) but does NOT
# personally perceive themselves as at risk (70.25% said No
# in Figure 5.6.1) AND is currently sexually active.
#
# This is the "optimistic bias" — documented by Weinstein (1987)
# and cited in Chapter 6.4.
# Your paper states: "The main challenge is not awareness, but
# the translation of that awareness into accurate personal
# risk perception."
# ===

def flag_knowledge_practice_gap(respondent):
    """
    Detects the knowledge-practice gap (optimistic bias) in a respondent.

    Parameters
    ----------
    respondent : dict
        A dictionary representing one survey respondent.
        Must contain keys:
          "believes_multi_partner_risk" : bool
          "self_perceived_risk"         : str ("Yes"/"No"/"Maybe")
          "sexual_active"               : bool

    Returns
    -------
    tuple : (bool, str)
        (True, explanation_string) if gap detected
        (False, "No gap detected") otherwise

    Study context
    -------------
    93.27% of your 333 students believed multiple partners = higher risk.
    But only 19.33% considered themselves personally at risk.
    The contradiction is sharpest among sexually active students:
    Table 5.8.4 shows even students engaging in casual sex — who showed
    the highest perceived risk (56.25%) — still had 37.5% denying risk
    entirely, despite their own high-risk behavior.
    """
    knows_risk = respondent.get("believes_multi_partner_risk", False)
    perceives_risk = respondent.get("self_perceived_risk", "No")
    is_active = respondent.get("sexual_active", False)

    # Core gap: knows risk in general, denies personal risk, yet is active
    if knows_risk is True and perceives_risk == "No" and is_active is True:
        return (
            True,
            "Optimistic bias: knows multiple-partner risk, "
            "denies personal vulnerability, yet sexually active."
        )

    # Partial gap: uncertain about personal risk while active
    if knows_risk is True and perceives_risk == "Maybe" and is_active is True:
        return (
            True,
            "Partial gap: knows risk, uncertain about personal "
            "vulnerability, yet sexually active."
        )

    # No gap: either not active, or correctly perceives personal risk
    return (False, "No gap detected")


# ===
# Function 4 — classify_condom_use_risk()
# Maps condom use consistency (from Question 53) to a
# clinical risk level.
#
# Raw response options from your questionnaire:
#   "Always", "Sometimes", "Never", "Not sexually active"
#
# In your Figure 5.7.1 (among sexually active respondents only):
#   Always    = 27.9%   → Low risk
#   Sometimes = 47.9%   → Moderate risk
#   Never     = 24.3%   → High risk
#
# In your Table 5.7.1 (all respondents):
#   Always    = 12.0%
#   Sometimes/Never = 31.08%
#   Not active      = 56.92%
#
# In your Table 5.8.1: consistent condom use was a significant
# predictor of STI testing (OR = 1.9, 95% CI: 1.0–3.4, p = 0.047)
# ===

def classify_condom_use_risk(consistency):
    """
    Maps condom use consistency to a clinical risk level.

    Parameters
    ----------
    consistency : str
        Raw survey response to Question 53:
        "Always", "Sometimes", "Never", or "Not sexually active"

    Returns
    -------
    str
        Risk classification: "Low risk", "Moderate risk",
        "High risk", or "Not applicable"

    Study context
    -------------
    Only 27.9% of sexually active students reported always using condoms.
    Nearly a quarter (24.3%) never used condoms.
    This inconsistency despite high HIV awareness (99.4%) reflects
    the knowledge-practice gap discussed in your Chapter 6.5.
    """
    risk_map = {
        "Always":              "Low risk",
        "Sometimes":           "Moderate risk",
        "Never":               "High risk",
        "Not sexually active": "Not applicable"
    }
    result = risk_map.get(consistency, None)
    if result is None:
        return f"Unknown response: '{consistency}' — check data cleaning"
    return result


# ===
# FUNCTION 5 — flag_sti_misconception()
# Detects whether a respondent holds specific STI transmission
# misconceptions that were prevalent in your study.
#
# The four most clinically significant misconceptions from
# your Tables 5.5.1–5.5.4:
#
#   1. Toilet seat transmission — syphilis (47.08% wrong, Table 5.5.1)
#   2. Toilet seat transmission — chlamydia (47.55% wrong, Table 5.5.2)
#   3. Toilet seat transmission — gonorrhoea (57.8% wrong, Table 5.5.4)
#   4. Razor/toothbrush — syphilis (68.73% wrong, Table 5.5.1)
#   5. Kissing transmits HIV (50.61% wrong, Table 5.5.3)
#   6. Vertical transmission unknown — syphilis (only 51.99% correct)
#   7. Vertical transmission unknown — chlamydia (only 42.68% correct)
#
# These misconceptions matter clinically because:
#   - Toilet seat myths stigmatize STI patients (Jabeen et al., 2022)
#   - Kissing/HIV myth increases irrational fear (Table 5.5.3)
#   - Vertical transmission gaps threaten neonatal outcomes
# ===

def flag_sti_misconception(respondent):
    """
    Identifies which specific STI misconceptions a respondent holds.

    Parameters
    ----------
    respondent : dict
        A dictionary representing one survey respondent.
        Expects boolean keys named with the convention:
          correct_[sti]_not_[route]  = True means correctly knows it's NOT a route
          correct_[sti]_[route]      = True means correctly knows it IS a route

    Returns
    -------
    tuple : (bool, list)
        (True, [list of misconception labels]) if any misconceptions found
        (False, []) if no misconceptions detected

    Study context
    -------------
    Your Chapter 6.3 concluded: "Misconceptions are not isolated to
    KNUST students. Misinformation about STI transmission through toilet
    seats or shared surfaces has been widely reported." The prevalence
    of these myths at 47–68% highlights the need for targeted
    myth-busting campaigns in university health education programmes.
    """
    misconceptions = []

    # Check 1: Syphilis via toilet seat myth
    # correct_syphilis_not_toilet = False means they think toilet seats DO spread syphilis
    if respondent.get("correct_syphilis_not_toilet") is False:
        misconceptions.append(
            "Syphilis-toilet-seat myth (47.08% in your study)")

    # Check 2: Chlamydia via toilet seat myth
    if respondent.get("correct_chlamydia_not_toilet") is False:
        misconceptions.append(
            "Chlamydia-toilet-seat myth (47.55% in your study)")

    # Check 3: Gonorrhoea via toilet seat myth
    if respondent.get("correct_gonorrhoea_not_toilet") is False:
        misconceptions.append(
            "Gonorrhoea-toilet-seat myth (57.8% in your study)")

    # Check 4: Syphilis via razor/toothbrush sharing
    if respondent.get("correct_syphilis_not_razor") is False:
        misconceptions.append(
            "Syphilis-razor/toothbrush myth (68.73% in your study)")

    # Check 5: HIV via kissing
    # 50.61% incorrectly believed kissing transmits HIV (Table 5.5.3)
    if respondent.get("correct_hiv_not_kissing") is False:
        misconceptions.append("HIV-kissing myth (50.61% in your study)")

    # Check 6: Vertical transmission — syphilis unknown
    if respondent.get("correct_syphilis_vertical_trans") is False:
        misconceptions.append(
            "Syphilis-vertical-transmission gap (51.99% correct in your study)")

    # Check 7: Vertical transmission — chlamydia unknown
    if respondent.get("correct_chlamydia_vertical_trans") is False:
        misconceptions.append(
            "Chlamydia-vertical-transmission gap (42.68% correct in your study)")

    if misconceptions:
        return (True, misconceptions)
    return (False, [])


# ===
# Part B — build_respondent_profile()
# A composite function that applies all five functions above
# to produce a complete clinical profile for one respondent.
#
# This is what your pipeline will do to all 333 respondents
# on Day 6. Today you test it on 5 manually-built respondents.
# ===

def build_respondent_profile(respondent):
    """
    Runs all five classification functions on a single respondent
    and returns a complete clinical profile dictionary.

    This function is the Python equivalent of running all your
    STATA recoding commands on a single observation.

    Parameters
    ----------
    respondent : dict
        A full respondent dictionary from your GROUP_17 cohort

    Returns
    -------
    dict
        The original respondent dictionary with six derived fields added:
          "risk_numeric"        : float
          "knowledge_tier"      : str
          "knowledge_pct"       : float
          "condom_risk_level"   : str
          "gap_present"         : bool
          "gap_explanation"     : str
          "misconceptions"      : list
          "misconception_count" : int
    """
    # Make a copy so we do not modify the original
    profile = dict(respondent)

    # Apply Function 1 — encode risk perception
    profile["risk_numeric"] = classify_self_risk(
        respondent.get("self_perceived_risk", "No")
    )

    # Apply Function 2 — classify knowledge
    tier, pct = classify_knowledge_level(
        respondent.get("knowledge_score", 0)
    )
    profile["knowledge_tier"] = tier
    profile["knowledge_pct"] = pct

    # Apply Function 3 — flag knowledge-practice gap
    gap, explanation = flag_knowledge_practice_gap(respondent)
    profile["gap_present"] = gap
    profile["gap_explanation"] = explanation

    # Apply Function 4 — classify condom risk
    profile["condom_risk_level"] = classify_condom_use_risk(
        respondent.get("condom_use_consistency", "Not sexually active")
    )

    # Apply Function 5 — flag misconceptions
    has_misconceptions, misconception_list = flag_sti_misconception(respondent)
    profile["misconceptions"] = misconception_list
    profile["misconception_count"] = len(misconception_list)

    return profile


# Part C — Five Test Respondents
# Each one represents a distinct profile from your study's
# demographic and behavioral distribution.
#
# These are not random — they are deliberately constructed
# to test different branches of your five functions:
#
# R1: Health Sciences, not active, high knowledge, denies risk
#     → Tests gap function (False — not active, gap not applicable)
#     → Tests misconception function (some myths possible)
#
# R2: Humanities, casual sex, low knowledge, perceives risk
#     → Tests gap function (False — correctly perceives risk)
#     → Tests condom risk (Never → High risk)
#
# R3: Engineering, committed relationship, moderate knowledge, denies risk
#     → Tests gap function (True — active, knows risk, denies it)
#     → Your Table 5.8.4: committed non-married → 22.89% at risk
#
# R4: Science, not active, high knowledge, no misconceptions
#     → Tests misconception function (False — no myths)
#     → Best-case respondent from Health Sciences adjacent background
#
# R5: Postgraduate, not active, moderate knowledge, uncertain risk
#     → Tests Maybe encoding in classify_self_risk
#     → Your Figure 5.6.1: 10.43% said Maybe
# ===

test_respondents = [
    # Respondent A — Health Sciences female, Level 200, not sexually active
    # Represents the 40.24% College of Health Sciences (Table 5.2.3)
    # and the 67.57% not engaging in sexual activity (Figure 5.2.3)
    {
        "id":                        "TEST-A",
        "gender":                    "Female",
        "age":                       21,
        "college":                   "Health Sciences",
        "level":                     200,
        "sexual_active":             False,
        "self_perceived_risk":       "No",
        "believes_multi_partner_risk": True,
        "knowledge_score":           17,
        "condom_use_consistency":    "Not sexually active",
        "ever_tested":               False,
        # Misconception flags (False = holds the misconception)
        "correct_syphilis_not_toilet":   False,   # holds toilet seat myth
        "correct_chlamydia_not_toilet":  False,   # holds toilet seat myth
        "correct_gonorrhoea_not_toilet": True,    # correctly knows NO toilet
        "correct_syphilis_not_razor":    True,    # correctly knows NO razor
        "correct_hiv_not_kissing":       True,    # correctly knows NO kissing
        "correct_syphilis_vertical_trans": True,   # correctly knows YES pregnancy
        # does not know vertical transmission
        "correct_chlamydia_vertical_trans": False,
    },
    # Respondent B — Humanities male, Level 400, casual sex, low knowledge
    # Represents the 4.8% engaging in casual sex (Figure 5.2.3)
    # Your Table 5.8.4: casual sex → 56.25% perceive themselves at risk
    {
        "id":                        "TEST-B",
        "gender":                    "Male",
        "age":                       23,
        "college":                   "Humanities",
        "level":                     400,
        "sexual_active":             True,
        "self_perceived_risk":       "Yes",
        "believes_multi_partner_risk": True,
        "knowledge_score":           9,
        "condom_use_consistency":    "Never",
        "ever_tested":               True,
        "correct_syphilis_not_toilet":   False,
        "correct_chlamydia_not_toilet":  False,
        "correct_gonorrhoea_not_toilet": False,
        "correct_syphilis_not_razor":    False,
        "correct_hiv_not_kissing":       False,   # holds HIV/kissing myth
        "correct_syphilis_vertical_trans": False,
        "correct_chlamydia_vertical_trans": False,
    },
    # Respondent C — Engineering male, Level 400, committed not married, denies risk
    # Your Table 5.8.4: committed non-married → 62.65% say NOT at risk
    # This respondent correctly tests the optimistic bias gap:
    # sexually active + knows risk + denies personal risk = gap
    {
        "id":                        "TEST-C",
        "gender":                    "Male",
        "age":                       22,
        "college":                   "Engineering",
        "level":                     400,
        "sexual_active":             True,
        "self_perceived_risk":       "No",
        "believes_multi_partner_risk": True,    # knows risk, yet denies personal
        "knowledge_score":           13,
        "condom_use_consistency":    "Sometimes",
        "ever_tested":               False,
        "correct_syphilis_not_toilet":   False,
        "correct_chlamydia_not_toilet":  True,
        "correct_gonorrhoea_not_toilet": False,
        "correct_syphilis_not_razor":    False,
        "correct_hiv_not_kissing":       True,
        "correct_syphilis_vertical_trans": False,
        "correct_chlamydia_vertical_trans": True,
    },
    # Respondent D — Science female, Level 300, not active, high knowledge
    # No misconceptions — represents the best-informed respondent profile
    {
        "id":                        "TEST-D",
        "gender":                    "Female",
        "age":                       20,
        "college":                   "Science",
        "level":                     300,
        "sexual_active":             False,
        "self_perceived_risk":       "No",
        "believes_multi_partner_risk": True,
        "knowledge_score":           19,
        "condom_use_consistency":    "Not sexually active",
        "ever_tested":               False,
        "correct_syphilis_not_toilet":   True,   # no myths — all correct
        "correct_chlamydia_not_toilet":  True,
        "correct_gonorrhoea_not_toilet": True,
        "correct_syphilis_not_razor":    True,
        "correct_hiv_not_kissing":       True,
        "correct_syphilis_vertical_trans": True,
        "correct_chlamydia_vertical_trans": True,
    },
    # Respondent E — Postgraduate female, uncertain risk, moderate knowledge
    # Represents the 5.11% postgraduate students (Table 5.2.2)
    # and the 10.43% who said Maybe to self-perceived risk (Figure 5.6.1)
    {
        "id":                        "TEST-E",
        "gender":                    "Female",
        "age":                       28,
        "college":                   "Health Sciences",
        "level":                     700,   # postgraduate
        "sexual_active":             True,
        "self_perceived_risk":       "Maybe",
        "believes_multi_partner_risk": True,
        "knowledge_score":           14,
        "condom_use_consistency":    "Always",
        "ever_tested":               True,
        "correct_syphilis_not_toilet":   True,
        "correct_chlamydia_not_toilet":  True,
        "correct_gonorrhoea_not_toilet": True,
        "correct_syphilis_not_razor":    False,   # one lingering myth
        "correct_hiv_not_kissing":       True,
        "correct_syphilis_vertical_trans": True,
        "correct_chlamydia_vertical_trans": True,
    },
]


# ===
# Part D — Run the Pipeline on all five test respondents
# Print a formatted profile for each one.
# Read each output carefully and verify it matches your
# expectations based on the respondent's values above.
# ===

print("=" * 70)
print("GROUP_17 STI STUDY — RESPONDENT CLINICAL PROFILE PIPELINE")
print("KNUST 2025 | n=5 test cases (full n=333 will run on Day 6)")
print("=" * 70)

for respondent in test_respondents:
    profile = build_respondent_profile(respondent)

    print(f"\n{'─' * 60}")
    print(f"RESPONDENT: {profile['id']}  |  "
          f"{profile['gender']}, Age {profile['age']}  |  "
          f"{profile['college']}")
    print(f"{'─' * 60}")

    # Demographics
    print(f"  Level:              {profile['level']}")
    print(f"  Sexually active:    {profile['sexual_active']}")

    # Knowledge assessment
    print(f"\n  KNOWLEDGE ASSESSMENT:")
    print(f"    Raw score:        {profile['knowledge_score']}/20")
    print(f"    Percentage:       {profile['knowledge_pct']}%")
    print(f"    Tier:             {profile['knowledge_tier']}")

    # Risk perception
    print(f"\n  RISK PERCEPTION:")
    print(f"    Self-perceived:   {profile['self_perceived_risk']}")
    print(f"    Numeric encoding: {profile['risk_numeric']}")
    print(f"    Condom use:       {profile['condom_use_consistency']}")
    print(f"    Condom risk:      {profile['condom_risk_level']}")

    # Knowledge-practice gap
    print(f"\n  KNOWLEDGE-PRACTICE GAP:")
    if profile["gap_present"]:
        print(f"    ⚠ GAP DETECTED: {profile['gap_explanation']}")
    else:
        print(f"    No gap detected")

    # Misconceptions
    print(f"\n  MISCONCEPTION AUDIT:")
    print(f"    Count: {profile['misconception_count']}/7 checked")
    if profile["misconceptions"]:
        for myth in profile["misconceptions"]:
            print(f"    ✗ {myth}")
    else:
        print(f"    ✓ No misconceptions detected in checked items")


# ===
# Part E — Cohort-Level Summaries Across all five profiles
# This is what Day 5 will do across all 333 respondents
# using Pandas groupby. Today you do it manually so you
# understand what groupby is actually computing under the hood.
# ===

print("\n\n" + "=" * 70)
print("COHORT-LEVEL SUMMARY (n=5 test respondents)")
print("=" * 70)

# Apply pipeline to all five
profiles = [build_respondent_profile(r) for r in test_respondents]

# --- Knowledge tier distribution ---
print("\nKNOWLEDGE TIER DISTRIBUTION:")
tiers = {"High": 0, "Moderate": 0, "Low": 0, "Unknown": 0}
for p in profiles:
    tiers[p["knowledge_tier"]] += 1

for tier, count in tiers.items():
    pct = count / len(profiles) * 100
    print(f"  {tier:<10}: {count}  ({pct:.0f}%)")

# --- Gap prevalence ---
gap_count = sum(1 for p in profiles if p["gap_present"] is True)
print(f"\nKNOWLEDGE-PRACTICE GAP:")
print(
    f"  Gap present:  {gap_count}/{len(profiles)} respondents ({gap_count/len(profiles)*100:.0f}%)")
print(f"  Paper finding: the gap exists because 93.27% know risk")
print(f"  but only 19.33% feel personally at risk (your Chapter 6.4)")

# --- Condom risk distribution ---
print(f"\nCONDOM USE RISK DISTRIBUTION:")
condom_risks = {}
for p in profiles:
    level = p["condom_risk_level"]
    condom_risks[level] = condom_risks.get(level, 0) + 1

for level, count in sorted(condom_risks.items()):
    pct = count / len(profiles) * 100
    print(f"  {level:<20}: {count}  ({pct:.0f}%)")

# --- Misconception prevalence ---
print(f"\nMISCONCEPTION PREVALENCE (out of 7 checked myths):")
all_myths = []
for p in profiles:
    all_myths.extend(p["misconceptions"])

myth_counts = {}
for myth in all_myths:
    myth_counts[myth] = myth_counts.get(myth, 0) + 1

for myth, count in sorted(myth_counts.items(), key=lambda x: -x[1]):
    pct = count / len(profiles) * 100
    print(f"  {count}/{len(profiles)} ({pct:.0f}%): {myth}")

# --- Mean knowledge score ---
scores = [p["knowledge_score"]
          for p in profiles if p["knowledge_score"] is not None]
mean_score = sum(scores) / len(scores)
print(
    f"\nMEAN KNOWLEDGE SCORE: {mean_score:.1f}/20 ({mean_score/20*100:.1f}%)")
print(f"(On Day 18 you will compute this per gender/college using SciPy t-tests)")
print(f"(On Day 19 you will test if these differences are statistically significant)")

# --- Ever tested distribution ---
tested_count = sum(1 for p in profiles if p.get("ever_tested") is True)
print(
    f"\nSTI TESTING UPTAKE: {tested_count}/{len(profiles)} ever tested ({tested_count/len(profiles)*100:.0f}%)")
print(f"Compare to your paper: 31.19% ever tested (Table 5.7.1)")
