# Public Health Informatics: Epidemiological Modeling of STI Knowledge Gaps & Behavioral Risk Discrepancies Among Kwame Nkrumah University of Science and Technology Students

[![Python Ingestion Pipeline](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![R Biostatistical Inference](https://img.shields.io/badge/R%20Inference-4.3%2B-green.svg?style=flat-square&logo=r)](https://www.r-project.org/)
[![Database Architecture](https://img.shields.io/badge/SQL-3NF%20Compliant-orange.svg?style=flat-square&logo=postgresql)](https://en.wikipedia.org/wiki/Third_normal_form)
[![Academic Manuscript](https://img.shields.io/badge/Manuscript-PDF%20Included-red.svg?style=flat-square&logo=adobe-acrobat-reader)]()
[![Interactive Analytics Engine](https://img.shields.io/badge/Tableau-Dashboard%20Live-brightgreen.svg?style=flat-square&logo=tableau)](https://public.tableau.com/)
[![License: Open Science](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

# Project Overview & Institutional Framework

This repository hosts a fully reproducible public health informatics workspace processing cross-sectional epidemiological data regarding Sexually Transmitted Infections (STIs) within higher education demographics.
The analytical frameworks developed here are based directly on a formal research project submitted to the **Department of Obstetrics and Gynecology, School of Medical Sciences, College of Health Sciences, Kwame Nkrumah University of Science and Technology (KNUST)**, in partial fulfillment for the Bachelor of Science(Hons) in Physician Assistantship degree.

# Original Research Title

_"Awareness, Risk Perception and Preventive Measures for Sexually Transmitted Infections among Kwame Nkrumah University of Science and Technology Students"_ **Research Cohort:** $N=333$ active undergraduate survey respondents (`data/group17_clean.csv`).

# Primary Research Questions Addressed

1. **The Institutional Awareness Disparity:** Does formal academic enrollment within the university (e.g., Health Sciences vs. non_Health tracks) create a statistically significant difference in a student's true clinical knowledge of asymptomatic transmission vectors?
2. **The Risk-Behavior Friction Vector:** How effectively does a student's self-perceived risk profile correlate with their actual recorded behavioral metrics (e.g. barrier protection consistency, active partner counts over a trailing 24-month horizon)?
3. **The Structural Communication Gap:** Where are the strategic optimization points for campus clinical interventions when evaluating the divergence between high-reach media channels (Social Media) and high-trust validation sources (Healthcare Professionals)?

---

# Computational Repository Architecture

This workspace is explicitly compartmentalized into specialized research tiers to guarantee open-science transparency and analytical reproducibility:

```text
knust-sti-informatics/
│
├── data/                                 # Secure Study Sandbox Tier
│   ├── group17_clean.csv                 # Raw Survey Ingestion Target (N=333)
│   └── processed_cohort_data.csv         # Cleaned, Standardized Pipeline Matrix
│
├── docs/                                 # Institutional Literature Domain
│   └── KNUST_STI_Final_Manuscript.pdf   # Appended Departmental Research Paper
│
├── src/                                  # Automated Data Engineering Layer
│   └── pipeline.py                       # Automated Ingestion, Cleansing & Custom Feature Functions
│
├── notebooks/                            # Interactive Computational Analysis Workspaces
│   ├── 01_biostatistical_inference.ipynb # SciPy Non-Parametric Independence Testing
│   └── 02_predictive_modeling.ipynb     # Scikit-Learn Regularized Risk Profiling Classifiers
│
├── database/                             # Relational Storage & EHR Normalization Tier
│   ├── schema.sql                        # 3rd Normal Form (3NF) Entity-Relationship Schema
│   ├── seed_db.py                        # Automated Python Seeding & Ingestion Pipeline Engine
│   └── run_queries.py                    # Advanced Analytical SQL Join & Window Function Executor
│
├── reports/                              # Open-Science Document Compilation Room
│   └── report.Rmd                        # Mixed-Language R-Markdown Biostatistical Briefing
│
├── .gitignore                            # IRB Data Governance and Asset Protection Guidelines
└── requirements.txt                      # Python System Dependency Constraints
```

---

# Core Methodological & Technical Pipeline Details

1. Data Cleansing & Automation (src/pipeline.py)

- Zero Bias: Replaces manual spreadsheet editing with an automated Python pipeline to preserve data integrity
- Contingency Fixing: Fixes survey gaps programmatically (e.g. auto-defaulting partners counts to 0 if a respondent selected "Not sexually active"), safeguarding down-stream statistical variance.
- Feature Engineering: Condenses complex questionnaire logic into a unified behavioral risk score (Low, Moderate, High).
- Clinical Mapping: Standardizes symptom strings (e.g. painless chancres, discharge) into clean boolean features for modeling.

2. Biostatistical Inference (notebooks/01_biostatistical_inference.ipynb)

- Hypothesis Testing: Runs non-parametric $\chi^2$ tests of independence to evaluate clinical literacy across different university colleges.
- Algorithmic Rigor: Tracks cell frequencies programmatically and extracts exact asymptotic p-values to prove demographic knowledge gaps.

3. Supervised Machine Learning (notebooks/02_predictive_modeling.ipynb)

- Risk Profiling: Trains an $\ell_2$-regularized Logistic Regression classifier using demographic and pathogen awareness data to predict a student's internal risk perception state.
- Model Diagnostics: Validates predictive power using confusion matrices, F1-scores, and Area Under the ROC Curve (ROC-AUC Score).

4. Epidemiological Diagnostics (reports/report.Rmd)

- Language Bilingualism: Integrates R alongside Python to match standard public health lab workflows.
- Risk Analytics: Uses the epitools library to compute Wald Odds Ratios (OR) with exact 95% confidence intervals, tracking behavioral risks against biological sex.
- Academic Visuals: Renders high-resolution, publication-ready graphics natively using ggplot2.

5. Relational EHR Simulation (database/schema.sql)

- Database Design: Normalizes flat data rows into a relational structure meeting Third Normal Form (3NF) standards.
- System Constraints: Deploys strict data types, primary/foreign keys, and specific database search indexes to mimic real-world Electronic Health Record (EHR) environments.

---

# Verified Computational Checkpoints & Core Outputs

- Notebook 1: Descriptive Epidemiology & Biostatistical Baseline

* **Cohort Ingestion & Management:** This pipeline successfully ingests and profiles the baseline campus cohort dataset ($N = 333$), demonstrating professional compliance in handling large-scale, cross-sectional health datasets.
* **Sparsity Audit Validation:** Executed a comprehensive data completeness check verifying high biostatistical viability, identifying localized item non-response markers linked with disclosure stigma.
* **Actionable Stakeholder Insights:** Cross-factional analysis successfully mapped severe structural health resource unawareness peaking sharply within non-science faculties.
* **Epidemiological Gap Identification:** Behavioral evaluations exposed a distinct third-person illusion where high peer-risk perceptions failed to correlate with or drive personal diagnostic utilization.
* **Demographic Stratification:** Uncovered critical gender and age testing disparities, establishing the empirical baselines required to construct interactive public health dashboards.

- Notebook 2: ML Pipeline Initialization & Advanced Feature Engineering

* **Predictive Disease Modeling:** Initialized an end-to-end classification infrastructure utilizing scikit-learn, optimizing regularized predictive modeling pipelines for behavioral trend forecasting.
* **Advanced Feature Engineering:** Constructed the _Relationship Insulation Index_ ($\text{is\_partnered} \times \text{peer\_risk\_perception}$) to mathematically isolate cognitive risk blind spots among partnered student demographics.
* **Robust Preprocessing Pipelines:** Embedded automated `SimpleImputer` fields alongside feature scaling and One-Hot Encoding layers to preserve data variance without introducing participant selection bias.
* **Clinical Output Translation:** Extracted structural log-odds from a balanced Logistic Regression model ($\text{ROC-AUC} = 0.71$), translating weights into concrete Odds Ratios highlighting service awareness ($\text{OR} = 3.03$) as the primary driver of screening behavior.
* **Clinical Workflow Automation:** Deployed a synthetic patient profiling engine calculating individual screening probabilities ($52.3\%$ vs $70.7\%$) to simulate point-of-care clinical triage tracking.

- Relational Database Engine Verification Metrics
  Running the production multi-table inner joints and advanced analytical window functions on the 3NF database schema outputs the following automated public health intelligence matrix:

```text
========================= ANALYSIS 1: STRATIFIED PREVALENCE METRICS =========================
             Institutional College  Total Cohort  Mean Age  Clinic Awareness %  Screening Prevalence %
                   HEALTH SCIENCES           134      22.2                40.3                    41.0
    HUMANITIES AND SOCIAL SCIENCES            64      20.5                26.6                    34.4
        ARTS AND BUILT ENVIRONMENT            25      21.4                32.0                    24.0
                       ENGINEERING            33      22.1                36.4                    18.2
                           SCIENCE            58      20.6                29.3                    17.2
AGRICULTURE AND NATURAL RESOURCES            19      21.4                15.8                    15.8

========================= ANALYSIS 2: ADVANCED WINDOW FUNCTION RANKING =========================
             Institutional College  Partnered Mean Risk Perception  Risk Blindness Priority Rank
                           SCIENCE                            3.41                               1
    HUMANITIES AND SOCIAL SCIENCES                            3.59                               2
AGRICULTURE AND NATURAL RESOURCES                            3.75                               3
        ARTS AND BUILT ENVIRONMENT                            3.75                               3
                   HEALTH SCIENCES                            3.85                               5
                       ENGINEERING                            4.17                               6
```

- Operational Insight Translation: The relational analytics verify a prominent Intention-Behavior Action Gap within the Engineering and Science faculties (high awareness, rock-bottom testing rates) and isolates the College of Science at Priority Rank 1 for relationship-driven risk blindness.

---

# Interactive Public Health Reporting Dashboards

To translate these complex computational findings into actionable insights for university boards, clinicians, and community health stakeholders, an interactive visualization layer was engineered.

Key Interactive Panels Deployed

- The Information-Trust Inversion Panel: Illustrates the stark divergence between data exposure reach (Social Media) and validation credibility (Clinicians) to guide future public health resource allocations.

- Dynamic Cohort Slicing: Enables real-time filtering of clinical literacy levels across academic levels, genders, and colleges.

👉 [Click Here to Access the Live Deployed Tableau Public Dashboard Portfolio] (Insert Your Live Tableau URL Link Here)

# Step-by-Step Local Replication Protocols

Follow these steps to establish the environment and verify the mathematical reproducibility of the research pipeline:

1. Initialize Local Project Workspace & Virtual Environment

Bash
git clone [https://github.com/yourusername/knust-sti-informatics.git](https://github.com/yourusername/knust-sti-informatics.git)
cd knust-sti-informatics
python -m venv venv
source venv/bin/activate # On Windows Shell use: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

2. Trigger the Data Cleaning Pipeline Engine
   Verify that the raw survey document is located exactly at data/group17_clean.csv, then run the ingestion script:

Bash
python src/pipeline.py

3. Run the Computational Research Notebooks
   Launch your local Jupyter notebook server to evaluate or inspect the analytical code cells:

Bash
jupyter notebook notebooks/

4. Compile the Reproducible R-Markdown Briefing
   Execute the rendering pipeline from your R console to compile the updated statistical brief:

R
rmarkdown::render("reports/report.Rmd")

# Research Project Attributions & Group Members

This project was successfully executed by Group 17 of the PA Class of 2025 under the Department of Obstetrics and Gynecology, KNUST School of Medical Sciences:

- Abdul Mumin Raadia Mohammed
- Opare-Baidoo Emmanuel
- Thompson Sylvia Akua Amankwaa
- Afriyie Albert Dwamena

# Open Science License Parameters

The source code, automation engines, and relational schema designs within this workspace are distributed freely under the MIT Open-Science License Parameters. You are welcome to adapt, modify, and scale this pipeline architecture for academic research and public health informatics training workflows.

# Contact & Academic Correspondence

- Lead Portfolio Engineer: Afriyie Albert Dwamena

- Professional Designation: Licensed Health Professional / Physician Assistant

- Academic Matrix: Alumnus, Kwame Nkrumah University of Science and Technology (KNUST)

- Research Pipelines: Public Health Informatics, Clinical Workflow Automation, Behavioral Epidemiology Modeling, and Healthcare Relational Database Management Systems.

```

```
