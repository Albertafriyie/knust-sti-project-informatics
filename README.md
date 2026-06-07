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
│   └── schema.sql                        # 3rd Normal Form (3NF) Entity-Relationship System Schema
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
