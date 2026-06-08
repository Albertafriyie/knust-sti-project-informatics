# Day 1 - Modelling a single Group_17 respondent in Python
# All values taken from my paper's Tables 5.2.1 - 5.2.3
# and Figures 5.2.2 - 5.2.5

# ===
# Section A - Demographics
# These map directly to Questions 2-9 of questionnaire
# ===

respondent_id = "STI-001"
age = 21
gender = "Female"
level_of_study = 200
college = "Health Sciences"
relationship_status = "Single"
sexual_activity = "Not engaging in sexual activity"
partners_last_2yrs = 0
lifetime_partners = 0

# ===
# Section B - STI Awareness
# These map to Question 10 of questionnaire
# Values reflect the percentage awareness from my Figure 5.4.1
# True = this respondent has heard of this STI
# ===

aware_hiv = True
aware_syphilis = True
aware_gonorrhoea = True
aware_hepatitis_b = True
aware_chlamydia = True
aware_herpes = True
aware_hpv = False
aware_trichomoniasis = False

# ===
# Section B - STI Knowledge (transmission knowledge)
# These map to Questions 13-31 of questionnaire
# Encoded as the Correct answer the responded gave
# ===

# Transmission of HIV/AIDS (Questions 13–17)
knows_hiv_via_unprotected_sex = True
knows_hiv_not_via_mosquito = True
knows_hiv_via_needles = True
knows_hiv_not_via_hugging = True
knows_hiv_not_via_kissing = False

# Transmission of Syphilis (Questions 22–26)
knows_syphilis_via_sex = True
knows_syphilis_via_sore_kiss = True
knows_syphilis_not_via_razor = False
knows_syphilis_vertical_trans = False
knows_syphilis_not_toilet = False

# Transmission of Chlamydia (Questions 27–31)
knows_chlamydia_via_sex = True
knows_chlamydia_not_toilet = False
knows_chlamydia_vertical = False
knows_chlamydia_not_clothing = True
knows_chlamydia_not_food = True

# ===
# SECTION C — RISK PERCEPTION
# These map to Questions 48–52 of questionnaire
# ===

knust_community_risk_score = 4
self_perceived_risk = "No"
concern_level = 4
believes_multiple_partners = True
believes_condom_with_trusted = True

# ===
# SECTION D — PREVENTIVE BEHAVIORS
# These map to Questions 53–57 of questionnaire
# ===

condom_use_consistency = "Not sexually active"
ever_tested_sti = False
tested_positive = False
aware_testing_services = True
willing_to_disclose = "Yes"


# ===
# PART F — OUTPUT: Print a respondent summary
# Uses f-strings
# ===

# Basic summary line
summary_line = f"{respondent_id} | {gender}, Age {age} | {college} | Level {level_of_study}"
print(summary_line)

# Relationship and activity context
print(f"Relationship: {relationship_status} | Activity: {sexual_activity}")

# Risk perception summary — this is the heart of Chapter 6.4
print(f"Self-perceived risk: {self_perceived_risk}")
print(f"Concern level: {concern_level}/5")
print(f"Believes multiple partners = risk: {believes_multiple_partners}")

# The core contradiction your paper identified:
print(f"\nKey finding check:")
print(f"  Knows multiple partners = risk: {believes_multiple_partners}")
print(f"  But personally feels at risk:   {self_perceived_risk}")
if believes_multiple_partners == True and self_perceived_risk == "No":
    print("  --> OPTIMISTIC BIAS PRESENT (matches your Chapter 6.4 finding)")


# ===
# PART G — STRING OPERATIONS
# These are the operations Pandas uses under the hood
# when cleaning your survey text responses
# ===

# Problem: Real survey data is messy
# Your Google Form responses might have inconsistent capitalisation
messy_college = "  health sciences  "
messy_gender = "FEMALE"
messy_activity = " not engaging in sexual activity "

# Clean them (you will do this to 333 rows on Day 6)
clean_college = messy_college.strip().title()
clean_gender = messy_gender.strip().title()
clean_activity = messy_activity.strip()

print(f"\nCleaned values:")
print(f"  College:  '{clean_college}'")
print(f"  Gender:   '{clean_gender}'")
print(f"  Activity: '{clean_activity}'")

# Check: does cleaned gender match declared gender?
if clean_gender == gender:
    print("  --> Gender values match after cleaning")
else:
    print("  --> MISMATCH — cleaning introduced an error, check your logic")


# ===
# PART H — TYPE CONVERSION
# Survey data always arrives as strings from Google Forms
# You must convert to the correct type before analysis
# ===

# These came from your raw CSV as strings — they need conversion
age_from_csv = "21"
level_from_csv = "200"
concern_from_csv = "4"
partners_from_csv = "0"

# Convert to correct types
age_int = int(age_from_csv)
level_int = int(level_from_csv)
concern_int = int(concern_from_csv)
partners_int = int(partners_from_csv)

print(f"\nType conversion check:")
print(
    f"  age: '{age_from_csv}' (str) --> {age_int} (int) | type: {type(age_int)}")
print(f"  concern: '{concern_from_csv}' (str) --> {concern_int} (int)")

# Risk perception encoding — convert Yes/No/Maybe to numbers for analysis
# This mirrors what STATA does when I run logistic regression
risk_encoding = {"Yes": 1, "No": 0, "Maybe": 0.5, "I do not know": None}
risk_numeric = risk_encoding[self_perceived_risk]
print(
    f"\n  self_perceived_risk: '{self_perceived_risk}' --> {risk_numeric} (numeric)")
print(f"  This is how your Table 5.8.1 logistic regression encoded the outcome variable")

# ===
# PART I — AWARENESS PROFILE
# Build a list of which STIs this respondent knows about
# using the boolean variables declared above
# ===

# The STI names in order (matching Figure 5.4.1 order)
all_stis = ["HIV/AIDS", "Syphilis", "Gonorrhoea", "Hepatitis B",
            "Chlamydia", "Herpes", "HPV", "Trichomoniasis"]

# The corresponding awareness flags in the same order
all_flags = [aware_hiv, aware_syphilis, aware_gonorrhoea, aware_hepatitis_b,
             aware_chlamydia, aware_herpes, aware_hpv, aware_trichomoniasis]

# Build list of STIs this respondent is aware of
known_stis = [sti for sti, known in zip(all_stis, all_flags) if known is True]
unknown_stis = [sti for sti, known in zip(
    all_stis, all_flags) if known is False]

print(f"\nSTI Awareness Profile for {respondent_id}:")
print(f"  Aware of ({len(known_stis)} STIs):   {known_stis}")
print(f"  Unaware of ({len(unknown_stis)} STIs): {unknown_stis}")

total_stis = len(all_stis)
known_count = len(known_stis)
awareness_score_pct = (known_count / total_stis) * 100
print(
    f"  Overall awareness: {known_count}/{total_stis} = {awareness_score_pct:.1f}%")


# ===
# PART J — TRANSMISSION MISCONCEPTION AUDIT
# Identify which of this respondent's transmission beliefs
# are incorrect, based on your Tables 5.5.1 – 5.5.4
# ===

# Define what the CORRECT answer is for each question
# True = it IS a transmission route, False = it is NOT
correct_answers = {
    "HIV via unprotected sex":      True,
    "HIV via mosquito bites":       False,
    "HIV via needle sharing":       True,
    "HIV via hugging":              False,
    "HIV via kissing":              False,
    "Syphilis via unprotected sex": True,
    "Syphilis via sore/kiss":       True,
    "Syphilis via razor sharing":   False,
    "Syphilis via pregnancy":       True,
    "Syphilis via toilet seat":     False,
    "Chlamydia via unprotected sex": True,
    "Chlamydia via toilet seat":    False,
    "Chlamydia via childbirth":     True,
    "Chlamydia via clothing":       False,
    "Chlamydia via food/drinks":    False,
}

# This respondent's answers (using variables declared above)
respondent_answers = {
    "HIV via unprotected sex":      knows_hiv_via_unprotected_sex,
    "HIV via mosquito bites": not knows_hiv_not_via_mosquito,
    "HIV via needle sharing":       knows_hiv_via_needles,
    "HIV via hugging": not knows_hiv_not_via_hugging,
    "HIV via kissing": not knows_hiv_not_via_kissing,
    "Syphilis via unprotected sex": knows_syphilis_via_sex,
    "Syphilis via sore/kiss":       knows_syphilis_via_sore_kiss,
    "Syphilis via razor sharing": not knows_syphilis_not_via_razor,
    "Syphilis via pregnancy":       knows_syphilis_vertical_trans,
    "Syphilis via toilet seat": not knows_syphilis_not_toilet,
    "Chlamydia via unprotected sex": knows_chlamydia_via_sex,
    "Chlamydia via toilet seat": not knows_chlamydia_not_toilet,
    "Chlamydia via childbirth":     knows_chlamydia_vertical,
    "Chlamydia via clothing": not knows_chlamydia_not_clothing,
    "Chlamydia via food/drinks": not knows_chlamydia_not_food,
}

print(f"\nTransmission Knowledge Audit for {respondent_id}:")
incorrect = []
for question, correct in correct_answers.items():
    respondent_ans = respondent_answers[question]
    status = "CORRECT" if respondent_ans == correct else "INCORRECT"
    if status == "INCORRECT":
        incorrect.append(question)
    print(f"  {status:<10} {question}")

print(
    f"\n  Score: {len(correct_answers) - len(incorrect)}/{len(correct_answers)} correct")
if incorrect:
    print(f"  Misconceptions: {incorrect}")
