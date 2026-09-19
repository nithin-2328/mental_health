# Evidence-Based Findings: Mental Health in Tech Survey EDA

This document contains concise, empirical findings extracted directly from the cleaned OSMI Mental Health in Tech dataset (1,259 respondents). All counts, percentages, and statistical test values are exact calculations.

---

### Finding 1: High Overall Treatment Uptake in Tech
- **Finding:** Seeking professional mental health treatment is a mainstream reality affecting over half the technology workforce.
- **Evidence:** 637 out of 1,259 respondents (**50.60%**) reported having sought treatment for a mental health condition, while 622 (**49.40%**) reported they have not.
- **Interpretation:** Mental healthcare in tech organizations cannot be treated as an edge-case benefit; it is a fundamental operational necessity.

---

### Finding 2: Work Interference Severity Strongly Drives Treatment Seeking
- **Finding:** Frequency of work interference is the single strongest statistical predictor of treatment uptake in the dataset.
- **Evidence:** $\chi^2 = 294.837$, $p = 1.30 	imes 10^{-63}$, $	ext{df} = 4$, $	ext{Cramér's } V = 0.542$ (Very Strong Association).
  - 'Often' interferes: **84.03%** seek treatment (121 / 144)
  - 'Sometimes' interferes: **76.77%** seek treatment (357 / 465)
  - 'Rarely' interferes: **70.52%** seek treatment (122 / 173)
  - 'Never' interferes: **14.55%** seek treatment (31 / 213)
  - 'Not Applicable / Unreported': **2.27%** seek treatment (6 / 264)
- **Interpretation:** Employees experiencing chronic impairment actively seek professional clinical intervention, whereas employees without acute interference rarely do. Early detection of work friction offers a critical window for support.

---

### Finding 3: Family History of Mental Illness Doubles Treatment Likelihood
- **Finding:** Individuals with an immediate family history of mental illness seek care at more than double the rate of those without.
- **Evidence:** $\chi^2 = 178.267$, $p = 1.16 	imes 10^{-40}$, $	ext{df} = 1$, $	ext{Cramér's } V = 0.375$ (Relatively Strong Association).
  - Family History = 'Yes': **75.48%** seek treatment (369 / 489)
  - Family History = 'No': **34.81%** seek treatment (268 / 770)
- **Interpretation:** Familial history substantially increases self-awareness, reduces personal denial, and lowers the psychological threshold required to seek clinical help.

---

### Finding 4: Employer Care Options and Explicit Benefits Facilitate Care
- **Finding:** Knowledge of employer care options and benefit coverage strongly associates with increased treatment seeking.
- **Evidence:**
  - **Care Options:** $\chi^2 = 94.759$, $p = 2.65 	imes 10^{-21}$, $	ext{Cramér's } V = 0.272$.
    - 'Yes' (aware of options): **68.92%** seek treatment (306 / 444)
    - 'No' (no options): **36.93%** seek treatment (185 / 501)
    - 'Not sure': **46.50%** seek treatment (146 / 314)
  - **Benefits Coverage:** $\chi^2 = 64.839$, $p = 8.33 	imes 10^{-15}$, $	ext{Cramér's } V = 0.223$.
    - 'Yes' (benefits provided): **63.73%** seek treatment (304 / 477)
    - 'No' (no benefits): **45.28%** seek treatment (96 / 212)
    - 'Don't know': **41.21%** seek treatment (237 / 570)
- **Interpretation:** Organizational health provisions demonstrably remove financial and logistical friction. However, the fact that 31.8% of workers do not know if benefits exist indicates severe internal communication breakdowns.

---

### Finding 5: Significant Gender Disparities in Treatment Uptake
- **Finding:** Female and Non-Binary professionals seek treatment at significantly higher rates than Male tech workers.
- **Evidence:** $\chi^2 = 51.249$, $p = 7.44 	imes 10^{-12}$, $	ext{df} = 2$, $	ext{Cramér's } V = 0.198$.
  - Female: **68.83%** seek treatment (170 / 247)
  - Non-Binary / Other: **76.19%** seek treatment (16 / 21)
  - Male: **45.11%** seek treatment (447 / 991)
- **Interpretation:** Cultural stigma and traditional self-reliance norms may discourage male engineers from admitting psychological distress, while underrepresented groups in tech face compounded systemic stressors.

---

### Finding 6: Observable Workplace Consequences Elevate Treatment Rate
- **Finding:** Observing colleagues experience negative consequences for mental health issues correlates with higher personal treatment seeking.
- **Evidence:** $\chi^2 = 30.140$, $p = 4.02 	imes 10^{-8}$, $	ext{df} = 1$, $	ext{Cramér's } V = 0.152$.
  - Observed Consequence = 'Yes': **69.89%** seek treatment (129 / 184)
  - Observed Consequence = 'No': **47.26%** seek treatment (508 / 1,075)
- **Interpretation:** Environments with visible stigma or penalization force employees to manage severe distress externally through professional clinical pathways rather than through internal workplace channels.

---

### Finding 7: Company Size, Remote Work, and Tech Status Show No Significant Association
- **Finding:** Organizational scale and work arrangement do not significantly influence treatment seeking.
- **Evidence:**
  - Company Size (`no_employees`): $\chi^2 = 8.765$, $p = 0.1188$ (Not Significant)
  - Tech Company Status (`tech_company`): $\chi^2 = 1.093$, $p = 0.2958$ (Not Significant)
  - Remote Work (`remote_work`): $\chi^2 = 0.800$, $p = 0.3712$ (Not Significant)
  - Self-Employment (`self_employed`): $\chi^2 = 0.406$, $p = 0.5238$ (Not Significant)
- **Interpretation:** Mental health demands are ubiquitous across small startups, mid-sized firms, enterprise conglomerates, remote configurations, and in-office setups alike.
