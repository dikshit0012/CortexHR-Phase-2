# CortexHR — Phase 1: AI/ML Engineering & Analytics

> **Fictional data.** All company, people, payslip and tax data used in this repository is fictional ("Zenith Nova Technologies Pvt Ltd", part of Aura Workforce), generated for training. Any resemblance to real persons or businesses is accidental.

**Candidate:** Dikshit Kumar  
**Track:** AI/ML  
**Repository:** [https://github.com/dikshit0012/CortexHR-](https://github.com/dikshit0012/CortexHR-)  
**Phase:** Phase 1 Review Submission  

---

## 📌 Project Overview

CortexHR is an end-to-end AI/ML-driven HR analytics system designed to predict employee attrition, detect data anomalies, prevent data leakage, and establish robust, reproducible machine learning pipelines.

Phase 1 encompasses Tasks 1 through 5, delivering data audits, feature pipelines, baseline modeling, evaluation under class imbalance, and attendance anomaly detection.

---

## 📂 Repository Structure

```text
Phase 1 All task/
├── Task 1/              # Data Audit & Exploration (Leakage, duplicates, data quality)
│   ├── cortexhr-ml/     # Task 1 codebase, EDA notebooks, reports
│   └── reports/         # Task 1 Data Audit Report (PDF & DOCX)
├── task 2/              # Feature Engineering & Reusable Pipeline
│   └── files/           # Clean scikit-learn ColumnTransformer, CV data joins
├── task 3/              # Honest Baseline Models & Metrics
│   └── files/           # 5-fold stratified CV, Decision Tree vs Logistic Regression
├── task 4/              # Model Evaluation & Diagnostic Analysis
│   └── files/           # Cost-matrix evaluation, ROC-AUC, Manager Note
├── task 5/              # Attendance Anomaly Detection & Phase 1 Final Review
│   ├── data/            # Raw datasets
│   ├── reports/         # Final Review Report (PDF & DOCX), anomaly metrics & flagged records
│   ├── scripts/         # Anomaly detector runner & report generator
│   ├── src/             # Anomaly detector module (Z-score + IQR + Isolation Forest)
│   └── tests/           # Unit and regression test suite
├── task 6/              # Phase 2 - Payroll Outlier Detector (rules + Isolation Forest, per-error-type evaluation)
│   ├── src/             # Features, rules, model, evaluation, reporting
│   ├── scripts/         # run_task6.py
│   ├── tests/           # 90 tests (synthetic data; real-data tests skip without the workbook)
│   └── reports/         # Metrics, flagged records, comparison report (see task 6/README.md)
└── task 7/              # Phase 2 - Explain every flag: reason codes and money at risk (official sample_anomaly_results format)
    ├── src/ scripts/ tests/ docs/
    └── reports/         # Official output, 20-row sample, review sheet (see task 7/README.md)
```

> **This checkout is a Task 7 submission snapshot, not the complete tree shown above.** The `task 5/` and `task 6/`
> directories and the source workbook are not included. Task 7 imports those upstream detectors, so its end-to-end
> runner and integration tests need those files added before they can be run from this checkout. See
> [Task 7's README](./task%207/README.md) for the scope and verification limits of the retained reports.

---

## 🚀 Key Phase 1 Deliverables

The entries below describe the broader project; the Task 1–6 files are not part of this checkout, so their contents and metrics are not verified here.

| Task | Focus Area | Key Achievements & Deliverables |
|---|---|---|
| **Task 1** | Data Audit & Exploration | Detected 6 duplicate rows, 4 negative tenure errors, and 6 severe target leakage columns. Documented in `Task1_Data_Audit_Report.pdf`. |
| **Task 2** | Feature Pipeline | Built leak-free `ColumnTransformer` feature pipeline with time-series aggregates joined strictly inside CV folds. |
| **Task 3** | Honest Baselines | Evaluated Dummy classifier, balanced Logistic Regression (ROC-AUC ~0.712), and identified Decision Tree overfitting. |
| **Task 4** | Model Evaluation | Implemented business cost-matrix evaluation, threshold optimization, and manager briefing notes. |
| **Task 5** | Anomaly Detection & Review | Unsupervised multi-method anomaly detection (Isolation Forest, Z-score, IQR) with 100% test pass rate. Generated Phase 1 Comprehensive Review Report. |

## Phase 2 Deliverables

| Task | Focus Area | Scope in this snapshot |
|---|---|---|
| **Task 6** | Payroll anomaly detection | Referenced as Task 7's upstream detector; its source tree is not included in this checkout. |
| **Task 7** | Explain every flag | Reason codes, plain-language explanations, money-at-risk estimates, ranked official-format reports, and review materials. The end-to-end implementation depends on Task 5, Task 6, and the workbook, which are absent from this snapshot; see [task 7/README.md](./task%207/README.md). |

---

## 🧪 Running Tests & Scripts

To run the test suite for Task 5 anomaly detection:
```bash
pytest "task 5/tests"
```

To run the attendance anomaly detection pipeline:
```bash
python "task 5/scripts/run_task5.py"
```

To re-generate the Phase 1 Review Report:
```bash
python "task 5/scripts/generate_phase1_report.py"
```

To run the Task 6 payroll outlier detector and its tests:
```bash
python "task 6/scripts/run_task6.py"
pytest "task 6/tests"
```

To run Task 7 (reason codes and money at risk) and its tests:
```bash
python "task 7/scripts/run_task7.py"
python -m pytest "task 7/tests"
```
