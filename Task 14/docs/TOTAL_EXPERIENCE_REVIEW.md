## `total_experience_years` review

**Question.** The model's #2 most influential input is `total_experience_years`. It is never named in an employee's reasons as a precaution, because it could act as a proxy for age (which cannot be measured here). Is that policy enough, and what does the evidence show?

**What the data can and cannot show.** The workbook has **no age, date-of-birth or gender column for employees** (all 26 sheets scanned), so a link to age is **not measured here**. The concern rests on how the variable is built: experience accumulates over a working life. Nothing below demonstrates age discrimination, and nothing rules it out.

| evidence (real attrition-v2 model, 430 employees) | value |
|---|---|
| Importance rank by mean absolute SHAP (of 33) | **2** (2.97 percentage points; 8.9% of all SHAP) - after job level (3.42), before length of service (2.87) |
| Direction | more recorded experience -> **higher** model risk (rank correlation of value and contribution 0.98) |
| Correlated with (Spearman, scoring data) | job level 0.65, annual pay 0.59, tenure 0.50, previous employers 0.16 |
| Data quality | 17 employees record **less total experience than their tenure** (range 0.0-31.8 years, median 8.6) |
| Logistic coefficient per standard deviation, 5 ensemble members | 0.76, 0.44, 0.75, 0.50, 0.40 (all positive, but varies by almost a factor of 2) |
| Marginal signal in the training table (2,379 rows, 349 leavers) | AUC **0.49** - alone it does **not** separate leavers |
| Sign once tenure and job level are held fixed | +0.33 per SD, bootstrap 95% interval [-0.00, 0.59] - the lower end touches zero |
| If it were NOT suppressed | in the top-3 risk-raising drivers of **128** employees, the single top driver for **65** |
| All 7 suppressed features together | 6.9 percentage points of absolute SHAP per employee; the single largest contributor is a suppressed feature for **77** employees (18%), **55** of them `total_experience_years` |

**Why leaving it out of the explanations does not remove its influence.** The reasons are a post-processing step on top of the model: attrition-v2 still receives the feature and still uses it to compute every score and band. What-if on the real model (the model is untouched; only the input is altered): setting everyone's experience to the cohort median changes the predictions by **3.0 percentage points on average** (up to 16.0), moves **82 employees to a different band**, and keeps only **28 of the 43** highest-risk people in the High band. It is the 3rd most influential input by this measure as well. So the scores and High-risk list partly depend on it, while the displayed reasons do not mention it.

**What this means.**
* The suppression is a **presentation safeguard, not a fairness fix.** It stops the report from saying "experience raises risk", but it cannot undo the feature's effect on who is ranked High.
* Its contribution is **statistically fragile**: no marginal signal, a positive sign only after conditioning on tenure and job level, a bootstrap interval touching zero, and member-to-member variation. It looks like a statistical correction for tenure and level rather than a robust attrition signal. That is evidence about *predictive stability*, not about fairness.
* Job level (#1) and tenure (#3) are also correlated with experience (and plausibly with age); both remain nameable (tenure with the mandated neutral wording). The exclusion list is therefore **not a complete age-proxy control**.
* Not done and not claimed: no group-fairness audit (no protected attribute exists for employees), no age analysis, no retraining. A defensible next step for Task 13/HR/legal is to retrain **without** `total_experience_years` and compare ranking quality and who moves bands, and to fix the 17 inconsistent records. Task 14 must not change attrition-v2.
