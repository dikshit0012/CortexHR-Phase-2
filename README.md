# CortexHR - Tasks 1-15

This repository contains the CortexHR AI/ML project work for Tasks 1-15, arranged in numerical order at the repository root. **The shared Task 1-4 audit and modeling package is in `task04`; Phase 2 contains Tasks 5-10; Phase 3 contains Tasks 11-15.** The folders remain at the root so existing cross-task imports and paths continue to work. This is a collection of separate experiments and services, not one install-and-run application. Several projects rely on an authorized workbook, candidate datasets, or locally generated model artifacts.

The programs are for research and decision support. They are not production-ready HR systems and must not be used as the sole basis for employment, compensation, or other consequential decisions. Use only approved data and follow your organization's privacy and retention requirements.

## Repository layout

| Phase | Folder | Project | Setup and availability |
|---|---|---|---|
| Phase 1 | [`task04/`](task04/README.md) | <a href="https://github.com/dikshit0012/CortexHR-" target="_blank"> <button> Phase 1 repo</button></a>Attrition audit, feature pipeline, baselines, and evaluation package (Tasks 1-4) | Source and tests included. The authorized workbook, row-level outputs, notebooks, and generated reports are omitted. |
| Phase 2 | [`task05/`](task05/README.md) | Attendance anomaly detection | Source and synthetic tests included. The authorized workbook is needed to run the real-data pipeline. |
| Phase 2 | [`task06/`](task06/README.md) | Payroll outlier detection | Detailed setup in [`task 6/`](task06/task%206/README.md). Real-data runs need the authorized workbook. |
| Phase 2 | [`task07/`](task07/README.md) | Explanations for anomaly flags | Detailed setup in [`task 7/`](task07/task%207/README.md). Reuses Tasks 5-6; real-data runs need the workbook. |
| Phase 2 | [`task08/`](task08/task%208/README.md) | FastAPI anomaly service | Needs model artifacts built locally from the workbook and the Tasks 5-7 source in this checkout. |
| Phase 2 | [`task09/`](task09/README.md) | HR FAQ intent classifier | Use the canonical copy in `cortexhr_task9`; train its local model artifact before serving through Task 8. |
| Phase 2 | [`task10/`](task10/README.md) | Conversational HR integration | Mock service code is included, but its required CSV data and demo-user table are not. Requires separately approved mock inputs and integration endpoints. |
| Phase 3 | [`task11/`](task11/README.md) | Resume ranking | Source and synthetic tests included; the job, resume, and label CSVs must be obtained separately. |
| Phase 3 | [`task12/`](task12/README.md) | Resume fairness audit | Requires Task 11's data and the audit-pair CSV. The optional protected-attribute file is confidential and must stay outside Git. |
| Phase 3 | [`task13/`](task13/README.md) | Attrition model V2 | Uses the shared `cortexhr` package in `task04\src` (set `CORTEXHR_ML_SRC`); the authorized workbook and model artifact must be supplied/generated locally. |
| Phase 3 | [`task14/`](task14/README.md) | Attrition risk explanations | Requires Task 13's locally generated artifact and the authorized workbook; the shared package is in `task04\src`. |
| Phase 3 | [`task15/`](task15/README.md) | Fair-pay band recommendations | Requires the salary-training workbook sheet or an approved CSV; the protected-attribute audit input is optional for general training but required for the official fairness audit. |

## Set up and run

Use a separate virtual environment for each task. The task projects have different dependency ranges, and some use serialized scikit-learn artifacts that must be built and loaded with compatible library versions. Follow each task's README for its supported Python version, required data, environment variables, and exact run commands.

For example, from a clean checkout in Windows PowerShell:

```powershell
python -m venv .venv-task05
.\.venv-task05\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r task05\requirements.txt
python -m pytest task05\tests
```

The Task 5 tests use synthetic fixtures. Running its detector requires an approved local workbook:

```powershell
$env:CORTEXHR_WORKBOOK = 'C:\approved-data\02_CortexHR_AI_ML_Dataset.xlsx'
python task05\scripts\run_task5.py
```

The Task 6/7 nested READMEs include their own commands. Task 8 can be launched only after its artifacts have been built from the workbook; Task 9's model must also be trained locally before its chat route is available.

## Data, artifacts, and privacy

The master workbook, candidate and employee datasets, protected-attribute files, local models, and generated record-level reports are intentionally not supplied as general setup fixtures. Obtain them through the organization's approved channel, store them in access-controlled local paths, and configure the task-specific environment variables documented by each project. Do not commit raw or protected data, credentials, local model artifacts, or person-level outputs.

`.gitignore` excludes known local/private data paths while keeping setup documentation trackable. Ignore rules are not a substitute for checking Git status before publishing.

## Scope and verification

The code and existing reports are included as project evidence, but some reports are retained artifacts and cannot be regenerated without the omitted inputs. A clean clone therefore does not make every end-to-end pipeline runnable. Run the synthetic tests first, then run data-backed tests and pipelines only after obtaining the required authorized inputs. Check the relevant task README for known limitations and any data-dependent test exclusions.

## Latest local test evidence

[Phase 3 test report (Tasks 4, 12, 13 and 14; 2026-11-06)](Phase3_Task_Test_Report_2026-11-06.pdf) records the local test results, warning details, and the environment used for Task 13. These results depend on local data and the separately supplied Task 2-4 package; they are not results from a clean-clone CI run.
