# GROUP_17 STI Re-Analysis — Sprint Notes

Started: [today's date]

## Pre-Day Setup Complete

- Python 3.12 installed ✓
- VS Code installed ✓
- Project folder created ✓
- group17_sti_survey_raw.csv exported from STATA ✓
- Libraries installed ✓

f-strings let me embed variables inside text.
In my study: f"{respondent_id} scored {score}/20" is how I would
print a respondent summary. This is what my STATA output tables do
automatically — I am doing it manually first so I understand it.

## Day 1 — Reflection

### Date: [today's date]

### What ran successfully:

[Describe the output your code produced — what printed, what the values were]

### Connection to my paper:

[In 2–3 sentences: how does declaring variables in Python relate to
how your questionnaire was structured? What is the Python equivalent
of a questionnaire field?]

### One thing that confused me:

[Be specific. Not "Python was hard" — that is not useful.
Something like: "I was confused about why False vs 'False' matters"
or "I did not understand why I needed int() conversion"]

### Answer to my confusion:

[Look it up if needed — StackOverflow, the video, anything.
Write the answer. The act of writing it consolidates it.]

### The optimistic bias in code:

[Describe in one sentence what the if/else check in Part F detects
and why it matters clinically — what does it mean when
believes_multiple_partners is True but self_perceived_risk is "No"?]

## Day 2 — Reflection

### Date: [today's date]

### What ran successfully:

[Describe each output section and what it showed.
Be specific — what did the risk distribution look like?
What was the trust-vs-use gap for social media?]

### The dictionary-to-DataFrame connection:

[In your own words: how is a Python dictionary structurally
identical to one row in your STATA dataset? What is the key
and what is the value in terms of your questionnaire?]

### What Pandas is — confirmed by today:

[Now that you have built a list of 10 dictionaries manually,
what is Pandas doing when you call pd.read_csv()?
Write one sentence.]

### The trust-use gap finding:

[Your Section 5.3 discussed this. Today you encoded it in Python.
In 2 sentences: what does the gap between social media use (88%)
and trust (40.3%) mean for STI education interventions in Ghana?]

### One thing that confused me today:

[Be specific]

### How I resolved it:

[Be specific]

### What Day 3 will build on:

[In one sentence: you now have a list of dictionaries. Day 3
will add logic — if/else and functions — that transforms that
list. What kind of transformations do you anticipate?]

## Day 3 — Reflection

### Date: [today's date]

### Functions I wrote today (list all five with one sentence each):

1. classify_self_risk() — [what it does in your own words]
2. classify_knowledge_level() — [what it does]
3. flag_knowledge_practice_gap() — [what it does and which table it maps to]
4. classify_condom_use_risk() — [what it does]
5. flag_sti_misconception() — [what it does and how many myths it checks]

### The knowledge-practice gap function:

[In 2–3 sentences: which respondents triggered the gap flag?
What does that tell you about the conditions that create optimistic bias?
Why does the function NOT flag a non-active respondent even if they
deny personal risk — is that the right clinical decision?]

### Verify against your paper:

[Did TEST-C trigger the gap correctly?
Your paper Table 5.8.4 says 62.65% of committed non-married
students say NOT at risk. TEST-C has self_perceived_risk = "No"
and sexual_active = True. Did the function catch it?]

### What default parameters add:

[In one sentence: why does classify_knowledge_level() have
max_score=20 as a default parameter? What would you change it to
if you were grading a 15-question quiz?]

### Connection to Day 4:

[In one sentence: tomorrow you load 333 real respondents into Pandas.
These five functions will need to run on all 333. How will that work?]

### Connection to your paper's Chapter 4.7 (Ethical Consideration):

[Your paper stated: "Their privacy was protected as their personal
information are kept confidential and secured."
Looking at your raw CSV today: what personal information is in the file?
Is any of it directly identifying? What would you need to anonymise
before sharing the dataset publicly (e.g., on GitHub)?]

### Connection to your paper's Section 1.7 (Limitations):

[Your paper listed self-reporting bias as a limitation.
Did you see any evidence of this in today's data?
For example: are there inconsistencies between the sexual activity
question (Figure 5.2.3) and the condom use question (Figure 5.7.1)?
A student who reported "not engaging in sexual activity" but also
reported "Sometimes" on condom use would be internally inconsistent.
Did you find any such cases?]

### One finding that surprised you:

[Something unexpected in the raw data that your paper did not mention.
Be specific about which column and what you found.]

### What Day 5 will do with this data:

[In 2–3 sentences: tomorrow you will reproduce your paper's Table 5.2.1
through Table 5.8.4 using Pandas. Based on what you saw today,
which columns will you need to rename or clean before that is possible?]

When he covers boolean indexing:

### Boolean indexing in my study:

df[df['self_perceived_risk'] == 'No']
→ this selects only the 70.25% of my sample who denied personal risk
→ STATA equivalent: keep if self_perceived_risk == "No"
→ I need this to reproduce Table 5.8.4 — the sexually active sub-group

df[(df['sexual_active'] == True) & (df['self_perceived_risk'] == 'No')]
→ this selects the knowledge-practice gap sub-group from Chapter 6.4
→ Two conditions combined with & (and)
→ STATA equivalent: keep if sexual_active==1 & self_perceived_risk=="No"
When he covers .groupby():

### groupby in my study:

df.groupby('gender')['knowledge_score'].mean()
→ mean knowledge score per gender group
→ STATA equivalent: by gender: summarize knowledge_score
→ This is the first step toward my Table 5.8.2 t-test on Day 18

df.groupby('college')['ever_tested'].mean() \* 100
→ % tested per college
→ STATA equivalent: by college: tabulate ever_tested
→ On Day 18 I will run chi-square on this
When he covers pd.crosstab():

### pd.crosstab() in my study:

pd.crosstab(df['gender'], df['self_perceived_risk'], normalize='index') \* 100
→ This IS my Table 5.8.2 — Risk Perception × Gender
→ normalize='index' means: percentages within each gender row
→ Expected: Male At Risk 21.74%, Female At Risk 17.39%
→ STATA equivalent: tabulate gender self_perceived_risk, row

# DAY 6 — Data Cleaning Pipeline

# GROUP_17 STI KAP Study · KNUST 2025

# Supervisor: Dr. B.B. Ofosu Barko

#

# PURPOSE:

# Reads group17_sti_survey_raw.csv (never modified)

# Applies all cleaning and derivation steps in sequence

# Writes group17_clean.csv to data/ directory

# Every cleaning decision is documented with:

# - WHAT is being changed

# - WHY it is being changed (clinical or methodological reason)

# - WHAT the effect is on row/column count

#

# This pipeline is the computational equivalent of your

# Chapter 4 Methodology section. A reviewer who reads

# this file can audit every analytical decision you made.

#

# RULE: The raw file is NEVER modified. EVER.

# All changes are made to df (the in-memory copy).

# The clean file is written separately.
