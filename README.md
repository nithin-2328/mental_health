# Mental Health in Tech – Exploratory Data Analysis

A comprehensive, production-ready Exploratory Data Analysis (EDA), statistical association testing suite, and interactive Streamlit analytics dashboard examining mental health dynamics in the global technology industry.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Dataset & Features](#dataset--features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Data Cleaning & Preprocessing](#data-cleaning--preprocessing)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Statistical Analysis](#statistical-analysis)
- [Key Findings](#key-findings)
- [Streamlit Dashboard](#streamlit-dashboard)
- [Limitations & Future Scope](#limitations--future-scope)
- [How to Run](#how-to-run)
- [Author](#author)

---

## Project Overview
This project conducts an exhaustive empirical investigation into the Open Sourcing Mental Illness (OSMI) Mental Health in Tech survey. Through systematic data auditing, robust outlier treatment, categorical harmonization, and rigorous hypothesis testing ($\chi^2$ test of independence and Cramér's $V$), this study evaluates how demographic traits, personal medical history, and employer policies influence mental health treatment uptake.

---

## Problem Statement
While software and technology companies frequently invest in health insurance and wellness programs, workplace stigma and information friction persistently hinder employees from seeking necessary mental healthcare. In high-pressure engineering environments, unaddressed mental distress manifests as work interference, burnout, reduced code quality, and elevated attrition. This project provides empirical evidence regarding which factors truly drive treatment uptake and how organizations can optimize their psychological support systems.

---

## Objectives
1. Quantify the prevalence of mental healthcare treatment across the technology sector.
2. Characterize the demographic landscape (Age, Gender, Geographic distribution).
3. Measure the impact of work interference severity and family history on care seeking.
4. Audit employee awareness and utilization of employer benefits, care options, and anonymity protections.
5. Statistically validate feature associations with treatment decisions using $\chi^2$ and Cramér's $V$ at $lpha = 0.05$.
6. Build a modern, interactive Streamlit analytics dashboard for intuitive business intelligence.

---

## Dataset & Features
- **Source:** OSMI Mental Health in Tech Survey (2014)
- **Observations:** 1,259 rows
- **Raw Features:** 27 columns (Processed: 33 attributes)
- **Primary Target:** `treatment` (Binary: Yes / No)
- **Core Feature Dimensions:**
  - *Demographics:* `Age_Cleaned`, `Age_Group`, `Gender_Cleaned`, `Country`, `state`, `self_employed`
  - *Clinical Indicators:* `family_history`, `work_interfere`
  - *Workplace Support:* `benefits`, `care_options`, `wellness_program`, `seek_help`, `anonymity`, `leave`
  - *Workplace Culture:* `mental_health_consequence`, `coworkers`, `supervisor`, `mental_health_interview`, `obs_consequence`

---

## Technologies
- **Python 3.10+**
- **Data Wrangling:** `pandas`, `numpy`
- **Visualization:** `matplotlib`, `seaborn`, `plotly`
- **Statistical Inference:** `scipy.stats`
- **Notebook Environment:** `jupyter`, `notebook`
- **Interactive Dashboard:** `streamlit`

---

## Project Structure
```
Mental_Health_in_Tech_EDA/
│
├── data/
│   ├── raw/
│   │   └── survey.csv                   # Original untouched survey dataset
│   └── processed/
│       ├── survey_cleaned.csv           # Cleaned, feature-engineered dataset
│       └── data_dictionary.csv          # Comprehensive data dictionary
│
├── notebooks/
│   ├── Sample_EDA_Submission_Template.ipynb   # Provided submission template
│   └── Mental_Health_in_Tech_EDA_Final.ipynb  # Executed final notebook (169 cells)
│
├── src/
│   ├── __init__.py                      # Package initializer
│   ├── data_cleaning.py                 # Reproducible data cleaning pipeline
│   ├── eda_analysis.py                  # Statistical testing & frequency metrics
│   └── visualization.py                 # Matplotlib & Seaborn plotting routines
│
├── app/
│   ├── app.py                           # Streamlit dashboard entry point
│   └── components.py                    # Reusable UI metric cards & Plotly charts
│
├── outputs/
│   ├── figures/                         # 15 publication-grade PNG figures
│   └── reports/
│       └── eda_summary.txt              # Auto-generated textual statistical summary
│
├── reports/
│   ├── project_report.md                # 12-section comprehensive formal report
│   └── findings.md                      # Evidence-based findings with exact values
│
├── requirements.txt                     # Project dependencies
├── README.md                            # Complete documentation & user guide
├── .gitignore                           # Git exclusions for Python/Jupyter/Streamlit
└── LICENSE                              # MIT License
```

---

## Data Cleaning & Preprocessing
- **Age Anomalies:** Outliers ranging from -1,726 to 99,999,999,999 were identified. Working age was bounded to 18–75 years; 8 invalid rows were imputed using the median of valid respondents (**31 years**). Engineered categorical `Age_Group` cohorts (`18-24`, `25-34`, `35-44`, `45-54`, `55+`).
- **Gender Harmonization:** 49 distinct free-text strings were standardized into `Male` (78.7%), `Female` (19.6%), and `Non-Binary/Other` (1.7%).
- **Missing Value Strategy:**
  - `comments`: 87.0% missing; filled with `'No Comment'` and added binary flag `has_comment`.
  - `state`: 40.9% missing (US-only); filled with `'Outside US / Not Applicable'`.
  - `work_interfere`: 21.0% missing; imputed as `'Not Applicable / Unreported'`.
  - `self_employed`: 1.4% missing; imputed using mode (`'No'`).

---

## Exploratory Data Analysis
- **Treatment Uptake:** 50.60% (637 / 1,259) of tech workers have sought professional mental healthcare.
- **Primary Demographic:** Median age is 31 years; 56.8% fall in the 25–34 age cohort.
- **Top Countries:** United States (59.7%), United Kingdom (14.7%), Canada (5.7%), Germany (3.6%).
- **Work Interference:** Over 62% experience at least occasional work interference due to mental health.

---

## Statistical Analysis
Tested at $lpha = 0.05$ with bias-corrected Cramér's $V$:
- **Work Interference:** $\chi^2 = 294.84, p = 1.30 	imes 10^{-63}, V = 0.542$ (Very Strong)
- **Family History:** $\chi^2 = 178.27, p = 1.16 	imes 10^{-40}, V = 0.375$ (Relatively Strong)
- **Care Options:** $\chi^2 = 94.76, p = 2.65 	imes 10^{-21}, V = 0.272$ (Moderate)
- **Benefits:** $\chi^2 = 64.84, p = 8.33 	imes 10^{-15}, V = 0.223$ (Moderate)
- **Gender:** $\chi^2 = 51.25, p = 7.44 	imes 10^{-12}, V = 0.198$ (Moderate)
- **Non-Significant Variables:** Company Size ($p=0.1188$), Tech Company ($p=0.2958$), Remote Work ($p=0.3712$), Self-Employed ($p=0.5238$).

---

## Key Findings
1. **Clinical Severity Dictates Care:** Employees reporting frequent work interference seek care at 84.0% versus 14.6% for those reporting none.
2. **Genetic Predisposition:** Family history increases treatment uptake from 34.0% to 75.5%.
3. **Information Accessibility:** Awareness of care options boosts treatment rates from 36.9% to 68.9%.
4. **Structural Neutrality:** Company size and remote working arrangements do not correlate with treatment rates.

---

## Streamlit Dashboard

### Purpose
An interactive, high-performance visualization layer providing stakeholders with dynamic exploration of the completed EDA.

### Features & Pages
1. **Overview:** Dynamic KPI cards (Total, Treated, Treatment Rate, Countries, Missing cells) and dataset health metadata.
2. **Demographics:** Interactive age distributions, cohort breakdowns, gender pie charts, and top-N country slider.
3. **Mental Health:** Treatment uptake by family history, work interference, gender, and age cohorts.
4. **Workplace & Support:** Evaluation of corporate benefits, care options, anonymity, and company size.
5. **Relationship Analysis:** Interactive bivariate explorer allowing users to select any Variable A and Variable B with normalized percentage or count views.
6. **Statistical Analysis:** Interactive hypothesis test inspector with $\chi^2$ statistics, p-values, degrees of freedom, and Cramér's $V$.
7. **Data Explorer:** Searchable, filterable data grid with custom column picker and CSV export functionality. Free-text comments are protected under data privacy controls.

### How to Run the Dashboard
From the project root directory:
```bash
# Install dependencies
pip install -r requirements.txt

# Launch Streamlit application
streamlit run app/app.py
```

---

## Limitations & Future Scope
- **Limitations:** Voluntary self-selection survey bias; cross-sectional observational design (non-causal); heavy geographic concentration in North America/UK.
- **Future Scope:** Longitudinal tracking of corporate wellness initiatives against engineering sprint velocity; NLP sentiment modeling on qualitative comments; predictive early-warning classification models.

---

## How to Run

### 1. Execute Data Cleaning & Statistical Pipeline
```bash
python src/data_cleaning.py
python src/eda_analysis.py
python src/visualization.py
```

### 2. View Executed Jupyter Notebook
Open `notebooks/Mental_Health_in_Tech_EDA_Final.ipynb` in VS Code or Jupyter Notebook. All 169 cells are pre-executed with complete visualizations and tables.

### 3. Run Interactive Dashboard
```bash
streamlit run app/app.py
```

---

## Author
**Data Analytics & Workplace Insights Consultant**  
Project: *Mental Health in Tech EDA Capstone*  
License: MIT
