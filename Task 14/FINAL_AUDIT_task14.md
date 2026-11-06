# Task 14 - final audit (generated)

24 of 24 output checks pass; 48 tests passed, 0 failed (2026-11-06). Task 13 workspace matches its recorded 31-file baseline (source: current Task 13 workspace, re-recorded 2026-11-06 after README.md and reports/task14.code-workspace changes; model.joblib sha256 a729dc24d2fc1b3e...).

## Validation checks
| # | check | result |
|---|---|---|
| 1 | exactly 430 employees | PASS |
| 2 | columns and order match the official sample | PASS |
| 3 | employee ids preserved (same set, same order) | PASS |
| 4 | no duplicate employee ids | PASS |
| 5 | prediction ids unique and sequential | PASS |
| 6 | risk scores numeric and within [0, 1] | PASS |
| 7 | risk scores rounded to 3 decimals like the sample | PASS |
| 8 | risk bands valid | PASS |
| 9 | band matches the unrounded probability (official helper, monotone) | PASS |
| 10 | SHAP additivity: base + sum(contributions) = prediction | PASS |
| 11 | model probability in the CSV equals the explained probability | PASS |
| 12 | no empty / NaN reason cells | PASS |
| 13 | no NaN anywhere | PASS |
| 14 | reasons readable (ends with a full stop, 20-340 characters) | PASS |
| 15 | no duplicated reason within an employee | PASS |
| 16 | three reasons for every employee where three drivers exist (shortfalls reported honestly) | PASS |
| 17 | no protected / sensitive terms, certainty claims or names in reasons | PASS |
| 18 | no technical feature names or jargon in reasons | PASS |
| 19 | every tenure reason carries the neutral sentence | PASS |
| 20 | model version is attrition-v2 | PASS |
| 21 | human review requirement + mandatory notice present on every row | PASS |
| 22 | human_review_required = true for all (internal report) | PASS |
| 23 | every named feature is allowed by the policy | PASS |
| 24 | reason direction matches the SHAP sign | PASS |

## Most influential features
| feature | mean |SHAP| (percentage points) | may be named in reasons |
|---|---|---|
| Job level | 3.42 | True |
| Total experience | 2.97 | False |
| Length of service | 2.87 | True |
| Latest engagement score | 2.52 | True |
| Pay compared with role mid-point | 2.24 | True |
| Manager changes | 1.96 | True |
| Role | 1.96 | True |
| Work mode | 1.65 | True |

### Files inspected
| file / source | role | how it was used | finding |
|---|---|---|---|
| GitHub repo `CortexHR-Phase-2` (cloned) | tasks 5-10, plus Task 11/12 written earlier | listed + searched | contains NO Task 13, Task 4 or model artifact, so Task 13 was taken from the uploaded zip |
| `task_13.zip`: `task 13/README.md` | Task 13 documentation | read | model choice rule, usage, limitations, `load_model`/`predict_attrition` entry points |
| `task_13.zip`: `src/attrition_v2/model_versioning.py`, `config.py` | Task 13 loader and scoring code | read + imported | official scoring path reused (no duplication) |
| `task_13.zip`: `model_artifacts/attrition-v2/model.joblib`, `metadata.json`, `metrics.json` | the trained model | loaded + read | CalibratedClassifierCV, 5 members, 33 features, version attrition-v2 |
| `cortexhr-ml_day4.zip`: `cortexhr-ml/src/cortexhr/` (features, monthly, ...) | Task 2/4 feature pipeline stored inside the model | listed + imported | needed to unpickle and to build the scoring table |
| `README.md`, `requirements.txt`, `pytest.ini`, `docker-compose.yml`, `Dockerfile`, `_gitignore`, `_dockerignore` | Task 1/2 project conventions | read (Dockerfile / ignore files listed only) | layout and dependency conventions |
| `verification_audit.md` | earlier verification report | opened (head only) | context only; not used as evidence |
| Workbook `CortexHR_Dataset.xlsx` - sheet `attrition_scoring_2026` | the 430 employees to score | read + validated | 430 rows, unique ids, 34 columns |
| Workbook - sheet `sample_attrition_risk` | official output format | read + schema copied | 11 columns, order, id format, rounding, band counts |
| Workbook - sheets `data_dictionary`, `README` | column meanings, CX-13/CX-14 notes | read | units and meanings used for wording |
| Workbook - sheet `attrition_dataset` | Task 13 training table | read (analysis only) | used for the total_experience_years association check |
| Workbook - column scan of all 26 sheets | search for age / DOB / gender | scanned | no employee age, date of birth or gender column exists |
| `cortexhr_helpers.py` | official `risk_bands()` | read; copied verbatim into `src/cortexhr_task14/` | unchanged; `risk_bands` used as is |

### Risk-band distribution
| band | employees | share | lowest score | highest score | rule (official helper) |
|---|---|---|---|---|---|
| High | 43 | 10.0% | 0.240 | 0.491 | top 10% of scores |
| Medium | 86 | 20.0% | 0.149 | 0.238 | next 20% |
| Low | 301 | 70.0% | 0.006 | 0.149 | the rest |

Helper cut-offs for this batch: High >= 0.2385 (90th percentile), Medium >= 0.1486 (70th percentile). Bands are rank-based, so they describe position in these 430 employees, not an absolute probability.

### Ten example employee explanations
Real rows of `attrition_risk_sample_10.csv` (High 4 / Medium 3 / Low 3, evenly spaced by score). Every one requires human review; the notice in the CSV's `model_note` applies to each.

| employee | score | band | reasons (SHAP contribution, percentage points) |
|---|---|---|---|
| EMP-0639 | 0.491 | High | 1. Recorded job level (1), which is on the lower side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+10.2 pp) 2. Recorded overtime of 11.0 hours per month over the last 3 months, which is on the higher side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+6.7 pp) 3. Recorded length of service (12 months) is contributing to a higher-than-average estimate in this model. Length of service alone does not indicate an intention to leave. (+4.1 pp) |
| EMP-0588 | 0.328 | High | 1. Number of manager changes in the last 12 months (2), which is on the higher side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+9.1 pp) 2. Most recent engagement survey score of 2.3 out of 5, which is on the lower side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+7.4 pp) 3. Recorded job level (2) is contributing to a higher-than-average predicted attrition risk. (+3.9 pp) |
| EMP-0464 | 0.264 | High | 1. Recorded change in monthly attendance over the last 3 months (+45.4 percentage points) is contributing to a higher-than-average predicted attrition risk. This is an unusually large change, so the underlying attendance records may be worth checking. (+7.3 pp) 2. Most recent engagement survey score of 2.5 out of 5, which is on the lower side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+5.4 pp) 3. Recorded overtime of 7.0 hours per month over the last 3 months, which is on the higher side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+4.4 pp) |
| EMP-0368 | 0.240 | High | 1. Number of manager changes in the last 12 months (3), which is on the higher side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+13.0 pp) 2. The employee's role group (R041) is associated with a higher-than-average predicted attrition risk in the data the model learned from; this is a group-level pattern, not a finding about this individual. (+6.7 pp) 3. Most recent engagement survey score of 2.6 out of 5, which is on the lower side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+4.8 pp) |
| EMP-0041 | 0.238 | Medium | 1. Number of manager changes in the last 12 months (4), which is on the higher side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+17.4 pp) 2. Recorded job level (1), which is on the lower side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+7.9 pp) 3. Recorded work mode (Onsite) is contributing to a higher-than-average predicted attrition risk. (+3.3 pp) |
| EMP-0306 | 0.185 | Medium | 1. Recorded job level (2) is contributing to a higher-than-average predicted attrition risk. (+3.3 pp) 2. Recorded pay of 0.86x the role mid-point, which is on the lower side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+2.8 pp) 3. Number of manager changes in the last 12 months (1), which is on the higher side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+2.8 pp) |
| EMP-0725 | 0.149 | Medium | 1. Recorded length of service (1 month) is contributing to a higher-than-average estimate in this model. Length of service alone does not indicate an intention to leave. (+4.2 pp) 2. Recorded job level (2) is contributing to a higher-than-average predicted attrition risk. (+3.0 pp) 3. No pay raise is recorded since joining and this is contributing to a higher-than-average predicted attrition risk. (+2.4 pp) |
| EMP-0420 | 0.149 | Low | 1. Number of manager changes in the last 12 months (1), which is on the higher side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+2.5 pp) 2. The employee's role group (R007) is associated with a higher-than-average predicted attrition risk in the data the model learned from; this is a group-level pattern, not a finding about this individual. (+2.5 pp) 3. Recorded work mode (Onsite) is contributing to a higher-than-average predicted attrition risk. (+2.5 pp) |
| EMP-0585 | 0.084 | Low | 1. The employee's role group (R030) is associated with a higher-than-average predicted attrition risk in the data the model learned from; this is a group-level pattern, not a finding about this individual. (+4.4 pp) 2. Recorded length of service (20 months) is contributing to a higher-than-average estimate in this model. Length of service alone does not indicate an intention to leave. (+1.6 pp) 3. Average recorded working time over the last 3 months (8.7 hours a day), which is on the higher side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+0.8 pp) |
| EMP-0179 | 0.006 | Low | 1. Most recent engagement survey score of 2.7 out of 5, which is on the lower side compared with other active employees, is contributing to a higher-than-average predicted attrition risk. (+1.3 pp) 2. Recorded work mode (Onsite) is contributing to a higher-than-average predicted attrition risk. (+1.0 pp) 3. The employee's department (D06) is associated with a higher-than-average predicted attrition risk in the data the model learned from; this is a group-level pattern, not a finding about this individual. (+0.8 pp) |

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
