# Mental Health in Tech: Comprehensive Exploratory Data Analysis Report

## 1. Project Title
**Mental Health in Tech Survey: Exploratory Data Analysis, Statistical Association Testing, and Workplace Dynamics**

---

## 2. Introduction
Mental health within high-intensity technical disciplines has emerged as one of the most critical determinants of employee well-being, organizational velocity, and sustainable talent retention. Software engineering, data analytics, product management, and IT operations are characterized by intense cognitive demands, tight continuous integration sprint cadences, high-stakes production deployments, and increasingly isolated remote or hybrid configurations. 

Despite the widespread prevalence of psychological fatigue, imposter syndrome, anxiety, and depressive disorders, technical environments historically operated under deep-seated cultural stigma. Employees frequently fear that acknowledging a mental health challenge could jeopardize career velocity, promotion candidacy, or team reputation. 

This project delivers an end-to-end empirical analysis of the Open Sourcing Mental Illness (OSMI) Mental Health in Tech survey. By examining 1,259 individual respondents across 48 countries, this research decodes the demographic landscape, quantifies treatment uptake rates, evaluates the efficacy and awareness of employer-sponsored mental health benefits, and statistically identifies the strongest predictors of mental healthcare utilization.

---

## 3. Problem Statement
Despite corporate investments in Employee Assistance Programs (EAPs) and wellness benefits, technology companies face persistent hurdles in employee mental health support:
1. **Awareness Gap:** While many companies purchase mental health coverage, a large portion of the workforce remains uninformed regarding how to access care or whether such coverage even exists.
2. **Confidentiality and Career Stigma:** Technical staff routinely express concern that seeking care or discussing mental struggles with supervisors could result in observable workplace consequences or negative interview evaluations.
3. **Operational Drag from Work Interference:** Untreated mental conditions manifest as cognitive exhaustion and presenteeism (working while impaired), which reduces code quality, causes sprint delays, and triggers abrupt turnover.

The business objective is to analyze the empirical survey evidence to understand which demographic and workplace factors facilitate or inhibit mental health treatment, and to provide human resources (People Operations) and engineering leadership with concrete, data-backed interventions.

---

## 4. Objectives
- **Prevalence Estimation:** Determine the proportion of technology professionals actively seeking mental healthcare treatment.
- **Demographic Cohort Profiling:** Characterize age distributions, gender representation, and geographic concentrations across tech workers.
- **Interference Measurement:** Quantify how frequently mental conditions interfere with work duties and how interference severity drives treatment urgency.
- **Support System Evaluation:** Audit employer provisions including mental health benefits, care options, wellness initiatives, and anonymity protections.
- **Hypothesis Testing:** Formulate and test statistical hypotheses using Chi-Square tests of independence and Cramér's V effect sizes at significance threshold $lpha = 0.05$.
- **Strategic Recommendations:** Deliver non-causal, evidence-based recommendations to build safe, psychologically healthy engineering cultures.

---

## 5. Dataset Description
The underlying dataset originates from the 2014 Open Sourcing Mental Illness (OSMI) Mental Health in Tech survey:
- **Total Submissions:** 1,259 rows
- **Total Attributes:** 27 raw columns (33 processed attributes after feature engineering)
- **Target Variable:** `treatment` (Binary: Yes / No)
- **Key Dimension Types:**
  - *Demographics:* `Age`, `Gender`, `Country`, `state`, `self_employed`
  - *Employment Structure:* `no_employees` (Company Size), `tech_company`, `remote_work`
  - *Clinical / Personal:* `family_history`, `work_interfere`
  - *Employer Support:* `benefits`, `care_options`, `wellness_program`, `seek_help`, `anonymity`, `leave`
  - *Workplace Climate:* `mental_health_consequence`, `phys_health_consequence`, `coworkers`, `supervisor`, `mental_health_interview`, `phys_health_interview`, `mental_vs_physical`, `obs_consequence`
  - *Qualitative:* `comments` (Open-ended text)

---

## 6. Data Cleaning & Preprocessing
To ensure absolute data integrity and reproducibility, the raw dataset underwent systematic cleaning via `src/data_cleaning.py`:

1. **Age Anomaly Treatment:**
   - Inspection revealed extreme invalid entries ranging from **-1,726** to **99,999,999,999** years.
   - Working adult boundaries were defined between **18 and 75 years**. Exactly 8 outlier records (<18 or >75) were identified.
   - Outliers were imputed using the median of valid respondents (**31 years**), avoiding row deletion.
   - Cleaned continuous age (`Age_Cleaned`) has a mean of **32.07 years**, standard deviation of **7.27 years**, and range of **18 to 72 years**.
   - Binned into 5 demographic cohorts: `18-24` (156, 12.4%), `25-34` (715, 56.8%), `35-44` (320, 25.4%), `45-54` (51, 4.1%), and `55+` (17, 1.4%).

2. **Gender Standardization:**
   - Raw free-text entries contained 49 distinct string variations with typos, casing discrepancies, and descriptive phrases (e.g., 'Cis Male', 'm', 'Mail', 'Femake', 'cis-female/femme', 'Trans woman', 'Enby').
   - Mapped into three standardized cohorts:
     - **Male:** 991 respondents (78.7%)
     - **Female:** 247 respondents (19.6%)
     - **Non-Binary / Other:** 21 respondents (1.7%)

3. **Domain-Grounded Missingness Imputation:**
   - `comments`: 1,095 missing (87.0%). Imputed with `'No Comment'` and retained an engineered binary flag `has_comment` (1=provided, 0=none).
   - `state`: 515 missing (40.9%). Non-US respondents do not have a US state; imputed with `'Outside US / Not Applicable'`.
   - `work_interfere`: 264 missing (21.0%). Survey skip-logic directed individuals without conditions to skip; imputed as `'Not Applicable / Unreported'`.
   - `self_employed`: 18 missing (1.4%). Imputed with the empirical mode (`'No'`).
   - Zero missing values remained in the processed dataset (`data/processed/survey_cleaned.csv`).

---

## 7. Exploratory Data Analysis (Univariate & Bivariate)

### 7.1 Baseline Treatment Prevalence
- **Treatment Uptake:** 637 respondents (**50.60%**) have sought treatment for a mental health condition, while 622 (**49.40%**) have not.
- This establishes that mental healthcare needs are mainstream, requiring proactive enterprise-level infrastructure.

### 7.2 Demographic Findings
- **Age:** Heavily concentrated in early-to-mid career professionals (median 31.0 years). Over 56.8% fall in the 25–34 bracket.
- **Gender Disparity in Care:** While males represent 78.7% of the tech sample, their treatment uptake rate is **45.11%** (447/991). In contrast, females seek treatment at **68.83%** (170/247), and Non-Binary/Other individuals seek treatment at **76.19%** (16/21).
- **Geographic Concentration:** Over 80% of respondents originate from North America and the United Kingdom (US: 751, UK: 185, Canada: 72, Germany: 45).

### 7.3 Workplace Support & Policy Distribution
- **Mental Health Benefits:** 477 respondents (37.9%) report employer-provided benefits, 212 (16.8%) report no benefits, and 400 (31.8%) report they **"Don't know"**.
- **Care Options Awareness:** 444 (35.3%) report clear care options, 501 (39.8%) report no options, and 314 (24.9%) are **"Not sure"**.
- **Wellness Programs:** Only 229 respondents (18.2%) have formal employer wellness discussions on mental health; 842 (66.9%) report none.
- **Anonymity Protections:** Only 375 respondents (29.8%) believe their anonymity is protected; 819 (65.0%) do not know.

---

## 8. Statistical Hypothesis Testing
Chi-Square tests of independence ($\chi^2$) and bias-corrected Cramér's V coefficients were computed against the primary outcome variable (`treatment`). Significance threshold: $lpha = 0.05$.

| Feature Tested | $\chi^2$ Statistic | p-value | Degrees of Freedom | Cramér's V | Association Strength | Significant ($p < 0.05$) |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| **work_interfere** | **294.837** | **1.30e-63** | 4 | **0.542** | Very Strong Association | **Yes** |
| **family_history** | **178.267** | **1.16e-40** | 1 | **0.375** | Relatively Strong Association | **Yes** |
| **care_options** | **94.759** | **2.65e-21** | 2 | **0.272** | Moderate Association | **Yes** |
| **benefits** | **64.839** | **8.33e-15** | 2 | **0.223** | Moderate Association | **Yes** |
| **Gender_Cleaned** | **51.249** | **7.44e-12** | 2 | **0.198** | Weak-to-Moderate Association | **Yes** |
| **obs_consequence** | **30.140** | **4.02e-08** | 1 | **0.152** | Weak Association | **Yes** |
| **anonymity** | **26.422** | **1.83e-06** | 2 | **0.139** | Weak Association | **Yes** |
| **mental_health_consequence** | **22.327** | **1.42e-05** | 2 | **0.127** | Weak Association | **Yes** |
| **mental_vs_physical** | **17.458** | **1.62e-04** | 2 | **0.111** | Weak Association | **Yes** |
| **mental_health_interview** | **12.690** | **1.76e-03** | 2 | **0.092** | Negligible Association | **Yes** |
| **wellness_program** | **11.498** | **3.19e-03** | 2 | **0.087** | Negligible Association | **Yes** |
| **seek_help** | **10.934** | **4.22e-03** | 2 | **0.084** | Negligible Association | **Yes** |
| **coworkers** | **6.001** | **4.98e-02** | 2 | **0.056** | Negligible Association | **Yes** |
| Age_Group | 8.355 | 0.0794 | 4 | 0.059 | Negligible | No |
| no_employees (Company Size) | 8.765 | 0.1188 | 5 | 0.055 | Negligible | No |
| phys_health_interview | 3.400 | 0.1827 | 2 | 0.033 | Negligible | No |
| phys_health_consequence | 3.371 | 0.1854 | 2 | 0.033 | Negligible | No |
| tech_company | 1.093 | 0.2958 | 1 | 0.009 | Negligible | No |
| remote_work | 0.800 | 0.3712 | 1 | 0.000 | Negligible | No |
| supervisor | 1.726 | 0.4220 | 2 | 0.000 | Negligible | No |
| self_employed | 0.406 | 0.5238 | 1 | 0.000 | Negligible | No |

---

## 9. Key Findings
1. **Work Interference is the Leading Indicator of Treatment Need:**
   Employees reporting that mental health interferes 'Often' have an **84.03%** treatment uptake rate, compared to **14.55%** among those reporting 'Never'.
2. **Family Predisposition is Highly Predictive:**
   A positive family history of mental illness increases the likelihood of seeking treatment from **34.01%** to **75.48%**.
3. **Information Friction Suppresses Care:**
   Employees who know their care options seek treatment at **68.92%**, compared to **36.93%** when none exist, and **40.32%** when uncertain. Over 31.8% of respondents do not know if benefits exist.
4. **Structural Neutrality:**
   Company headcount (p=0.1188), tech company status (p=0.2958), and remote work (p=0.3712) show no significant relationship with treatment rates. Mental health challenges exist uniformly across all firm sizes and work models.

---

## 10. Limitations
- **Volunteer Response Bias:** As an online voluntary survey, individuals experiencing mental health symptoms may have been more motivated to participate.
- **Cross-Sectional Observational Design:** Data reflects a single time snapshot (2014); all statistical associations represent non-causal relationships.
- **Geographic Bias:** US (59.7%) and UK (14.7%) respondents predominate; inferences may not generalize directly to developing tech hubs in Asia or South America.

---

## 11. Future Scope
- **Longitudinal Employee Tracking:** Measure how targeted mental health interventions impact team velocity, pull request cycle times, and voluntary resignation rates over multiple quarters.
- **Qualitative NLP Analysis:** Apply topic modeling and sentiment analysis to the 164 unstructured text comments to identify specific workplace friction points.
- **Cross-Industry Comparative Studies:** Benchmark technology worker burnout metrics against healthcare, finance, and legal sectors.

---

## 12. Conclusion
Mental health conditions in the tech sector are widespread, with over 50.6% of respondents seeking professional treatment. The primary operational drivers of treatment seeking are the severity of work interference and personal family history. 

From an organizational standpoint, the presence of clear care options and explicit mental health benefits significantly empowers employees to seek help. However, substantial barriers remain: massive benefit unawareness, lack of guaranteed anonymity, and lingering workplace stigma. By establishing transparent care pathways, training engineering managers in empathetic referral protocols, and guaranteeing absolute confidentiality, technology leaders can safeguard employee well-being and build high-performance technical cultures.
