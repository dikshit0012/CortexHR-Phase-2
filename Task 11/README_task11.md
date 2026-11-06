# Task 11 - Rank resumes against job descriptions (CortexHR, Phase 3)

An **explainable, decision-support** resume ranking engine: TF-IDF similarity + required-skill overlap, evaluated against human
judgement labels, with a misranking analysis and a fairness audit. It is **not** an automatic hiring decision-maker.

## 1. Task objective
Read resumes and job descriptions, extract skills and (reported-only) experience, score and rank every resume for every job,
compare with human labels (Top-5 hits, Precision@5, Recall@5, NDCG@5), explain at least five misrankings, and avoid prohibited features.

## 2. Datasets (inspected, nothing invented) - `data/`
| file | rows | key columns |
|---|---|---|
| `job_descriptions.csv` | **10** jobs (J01-J10) | job_id, job_title, min_experience_years, required_skills, nice_to_have_skills, education_preference, work_location, description_text (no missing values) |
| `resumes.csv` | **185** resumes (RES-0001...) | resume_id, resume_text (+ name, email, city, college_tier, structured skills... ); only `certifications` has missing values (114) |
| `resume_job_labels.csv` | **555** labelled pairs (30% of the 1,850 possible) | resume_id, job_id, `human_suitability_score` 1-5, `shortlist` Y/N, required/nice_skill_coverage, reviewer_note |

> The task brief mentioned 3 jobs / 5 resumes; the supplied data has 10 / 185. Everything below uses the real data.

Findings that drive the design:
* `shortlist = Y` **is exactly** `human_suitability_score >= 4` (95 pairs). Binary relevance = shortlist; graded relevance = score.
* Each resume is labelled for ~3 jobs, so each job has a **labelled pool of 47-64 resumes**. Unlabelled pairs are *not* treated as non-relevant.
* `required_skill_coverage` / `nice_skill_coverage` / `reviewer_note` in the label file are derived from the structured skills column. They are
  **leakage risks** and are used nowhere in scoring (only in post-hoc diagnostics, always labelled "eval only").
* Every resume states "N years of experience"; all 185 parse correctly and match the structured column. Layouts: Clean 96, Two-column 25, Tables 25, Missing sections 21, All-caps 18.
* Task 9 was reviewed: its `clean_text` conventions (NFKC, lowercase, NaN-safe) are followed, but it is not imported because it applies a chatbot
  typo-correction dictionary built for FAQ data and would couple Task 11 to Task 9's folder layout. No Task 1-10 file was modified.

## 3. Technologies
Validated in this workspace with Python 3.14.6, pandas 3.0.5, NumPy 2.5.1, scikit-learn 1.9.0 (`TfidfVectorizer`, cosine similarity),
SciPy 1.18.0 (Spearman), and pytest 9.1.1. `requirements.txt` uses minimum versions rather than exact pins.

## 4. Pipeline
1. **Preprocessing** (`preprocessing.py`): NFKC, lowercase, special characters removed (keeps `+ # / & . -` inside skill names such as `CI/CD`, `C++`), whitespace collapsed.
   Name/contact fields and their free-text mentions, explicit age/date-of-birth and gender/pronoun references, college-tier phrases, and university/institution names are
   **redacted before skill extraction and TF-IDF**. Numbers are dropped from the TF-IDF text. The supplied `candidate_name` value is required to redact unlabelled name mentions.
2. **Skill extraction** (`skill_extractor.py`): reusable dictionary extractor with word-boundary matching (`sql` does not match `postgresql`), and a reviewed synonym table
   (`MS Excel` = `Excel`, `sklearn` = `scikit-learn`, `Postgres` = `PostgreSQL` ...). Ranking vocabulary = the brief's base skills + skills in job descriptions.
   Resume structured skills widen a **separate extraction-validation vocabulary only**; they do not affect candidate feature extraction or ranking.
3. **Experience** (`preprocessing.extract_experience_years`): only an explicit "N years of experience" statement, else the sum of explicit "(x yrs)" role durations, else `NaN`.
   A bare number is never read as experience (tested: "69 quarters", "87k predictions", "28%").
4. **Job processing** (`job_processor.py`): title, required skills, preferred skills, `min_experience_years`, text. Education preference and work location are
   **excluded from the scored job text** (degree/institution and region proxies).
5. **Matching** (`ranking_engine.py`): TF-IDF (unigrams+bigrams, sublinear tf, English stop-words) fitted on resumes + job texts only (no labels);
   cosine similarity in [0,1]; skill overlap = matched required skills / required skills.

### Final score
```
final_score = 0.60 * tfidf_similarity + 0.40 * required_skill_overlap        (both in [0, 1])
```
Required and preferred job skills are present in the job TF-IDF text; only required skills enter the separate overlap component.
Ties are broken by `resume_id`. 500 of 1,850 rows share an exactly equal score with another resume. *Correction (found in Task 12):* all 500 are the 25 bias-twin
pairs (`resume_bias_pairs`: same content, different name/tier) x 10 jobs x 2 resumes - not template effects. The 10 tied rows inside an evaluated top-5 are twin resumes.
Swapping the tie-break direction leaves every metric identical - `reports/tie_sensitivity.csv`.

**Design decision - experience:** years of experience are extracted and shown next to each candidate (and whether they meet `min_experience_years`) but **never enter the
score**. Spearman correlation between score and experience on the labelled pairs is 0.078 (p=0.067), i.e. negligible.

**Note on the nominal 60/40 weights:** the TF-IDF cosine is numerically small (mean 0.029, max 0.383) because job texts are long. Per job, the standard deviation of the
weighted TF-IDF term is 0.031 versus 0.090 for the weighted overlap term, so skill overlap drives ordering about 3x more than the nominal weights suggest.
The formula was kept as specified, not tuned.

## 5. Evaluation against human judgement
Interpretation: relevant = `shortlist == Y` (score 4-5) for Top-5 hits / Precision@5 / Recall@5; NDCG@5 uses `rel = score - 1` with gain `2^rel - 1`
(a linear-gain NDCG is also reported). Ranks are computed inside each job's labelled pool. Precision@5 divides by 5 (or fewer candidates).
Because most jobs have more than 5 shortlisted candidates, Recall@5 is capped (`max_possible_recall_at_5`).

| job | title | pool | relevant | Top-5 hits | P@5 | R@5 | max R@5 | NDCG@5 |
|---|---|---|---|---|---|---|---|---|
| J01 | Software Engineer | 64 | 7 | 5 | 1.00 | 0.714 | 0.714 | 1.000 |
| J02 | Senior Software Engineer | 47 | 3 | 2 | 0.40 | 0.667 | 1.000 | 0.885 |
| J03 | Data Analyst | 60 | 12 | 5 | 1.00 | 0.417 | 0.417 | 1.000 |
| J04 | ML Engineer | 62 | 16 | 5 | 1.00 | 0.312 | 0.312 | 0.819 |
| J05 | Product Manager | 57 | 9 | 5 | 1.00 | 0.556 | 0.556 | 0.760 |
| J06 | Customer Support Executive | 49 | 6 | 5 | 1.00 | 0.833 | 0.833 | 0.985 |
| J07 | HR Executive | 49 | 8 | 5 | 1.00 | 0.625 | 0.625 | 1.000 |
| J08 | Accountant | 55 | 9 | 4 | 0.80 | 0.444 | 0.556 | 0.903 |
| J09 | Account Executive | 57 | 14 | 5 | 1.00 | 0.357 | 0.357 | 0.886 |
| J10 | Digital Marketing Executive | 55 | 11 | 5 | 1.00 | 0.455 | 0.455 | 0.877 |
| **micro** | | 555 | 95 | **46 / 50** | **0.92** | **0.484** | 0.505 | **0.905** |
| **macro** | | 555 | 95 | **46 / 50** | **0.92** | **0.538** | 0.582 | **0.912** |

`ranking_quality.csv` reports per-job values, a micro row (aggregate counts/DCG), and a macro row (unweighted mean of job metrics; counts summed). Macro Recall@5
is the unweighted mean of the 10 job recalls; micro Recall@5 is 46 / 95 = 0.484. Micro NDCG@5 aggregates DCG and ideal DCG across jobs. Precision@5 is 0.920
both ways because each job contributes five slots. Random expected Precision@5 is 0.168. The same macro/micro summaries are recorded separately in
`reports/run_summary.json`. Ablation (report only, `ranking_quality_ablation.csv`):
TF-IDF only 45 hits / NDCG 0.854; skill overlap only 45 / 0.870; hybrid 46 / 0.912.

Caveats: the pools are small, labels are on templated synthetic resumes, and the 0.92 should not be extrapolated to real resumes.

## 6. Misranking analysis - `reports/misranking_analysis.csv`
Definition: with R = number of shortlisted candidates in a job's pool, a **missed shortlist** is a shortlisted candidate ranked outside the top R; a **false shortlist**
is a non-shortlisted candidate ranked inside the top R. **16 genuine cases were found (8 + 8)**, all listed with the required fields (job, resume, rank, human label, scores,
matched/missing skills, reason, improvement). No case has a human score <= 2 in the false-shortlist group: all 8 are "Partial match" (score 3), so these are disagreements
about degree of fit, not clear errors. The 8 most severe are summarised below (reasons are computed from measured fields; see the CSV for all columns).

| # | job / resume | type | rank (pool, R) | human | score / TF-IDF / overlap | measured reason | improvement |
|---|---|---|---|---|---|---|---|
| 1 | J08 / RES-0103 | false shortlist | 3 (R=9) | 3 | 0.501 / 0.169 / 1.0 | Overlap 1.0 vs structured-profile required-skill coverage 0.4: "Tally" credited from "Tally Prime Certified" and "Bank Reconciliation" from a resume bullet; 7 candidates below it were rated higher | Weight certification/bullet-only evidence lower and show it as "indirect" |
| 2 | J09 / RES-0012 | missed | 20 (R=14) | 5 | 0.211 / 0.086 / 0.4 | "Missing sections" resume with no SKILLS section: Lead Generation and Presentation Skills are in the structured profile (coverage 0.8) but not extracted from the scored text; Lead Generation is only evidenced indirectly ("qualified leads") | Section-aware parsing / manual-review flag; semantic bullet matching |
| 3 | J02 / RES-0119 | false shortlist | 3 (R=3) | 3 | 0.364 / 0.206 / 0.6 | Overlap equals structured-profile coverage (0.6); rated a partial match; one lower-ranked candidate was rated higher | Add degree-of-fit features; verify with reviewers |
| 4 | J09 / RES-0065 | false shortlist | 11 (R=14) | 3 | 0.422 / 0.170 / 0.8 | Overlap equals structured-profile coverage (0.8); partial match; 4 lower-ranked candidates rated higher | as above |
| 5 | J04 / RES-0130 | missed | 23 (R=16) | 4 | 0.243 / 0.139 / 0.4 | No SKILLS section: Python, scikit-learn, SQL listed in the structured profile (coverage 1.0) but not extracted from scored text; overlap 0.4 | Fallback to structured skills / manual review |
| 6 | J08 / RES-0087 | false shortlist | 8 (R=9) | 3 | 0.463 / 0.104 / 1.0 | Overlap 1.0 vs human 0.6: GST and Bank Reconciliation credited from bullets only | as #1 |
| 7 | J03 / RES-0101 | false shortlist | 11 (R=12) | 3 | 0.398 / 0.130 / 0.8 | Overlap equals structured-profile coverage (0.8); partial match | as #3 |
| 8 | J02 / RES-0090 | missed | 7 (R=3) | 4 | 0.170 / 0.150 / 0.2 | No SKILLS section: Python and REST APIs in profile (human 0.6) not extracted; overlap 0.2 | as #5 |

Other missed shortlists (RES-0060, RES-0045, RES-0125, RES-0061, RES-0182, human score 4) have overlap equal to the structured-profile coverage (0.6-0.8), so extraction is not the cause; their
TF-IDF similarity is below the median of the candidates placed in the top R, and reviewers shortlisted them despite partial required coverage (role/title fit is a *hypothesis*, not verified).

Skill-extraction validation (`reports/extraction_validation.csv`): recall against the structured skills column is 1.00 for Clean, Tables, Two-column and All-caps layouts and
**0.756 for "Missing sections"**; precision 0.94 (extra matches are mostly broader terms, e.g. "Communication" inside "Customer Communication"). Experience parsing matches 185/185.

## 7. Fairness considerations
* **Excluded from scoring:** candidate name, e-mail, city, gender, age/date of birth, college tier/reputation, institution names, photographs, religion, caste, education string.
  Gender and age are not present in the supplied data; explicit mentions in resume text are scrubbed. Structured columns (including college and demographic columns if supplied,
  certifications, stated experience, target family, title, company, layout, file format, and structured skills) are not scoring features. Permuting these columns leaves every score unchanged
  (test `test_structured_resume_columns_do_not_change_scores`). Changing a name/city/college in a resume does not change its score. Labels never reach the scoring modules (static + shuffled-label tests).
* **Excluding protected attributes does not make the system fair.** Proxy bias and disparate outcomes still need auditing. `reports/fairness_audit.csv` (descriptive, small groups) shows:
  * **Layout/format disparity (real):** of the human-shortlisted pairs, only 70% (7/10) from "Missing sections" resumes land in the top R, versus 96% for Clean resumes, and their mean score is 0.126 vs ~0.16.
    Human mean scores are similar (2.35 vs 2.33), so the gap comes from extraction, not merit. Resumes without a SKILLS section are systematically under-scored.
  * College tier (not used): shortlisted candidates captured in the top R: Tier 1 0.97, Tier 2 0.87, Tier 3 0.91 (28/29, 27/31, 32/35) - small samples; monitor, do not conclude.
  * Gender and age cannot be audited (no such columns). Real deployment needs them collected lawfully for audit only.
* **Years of experience alone should not rank candidates:** it rewards tenure over skill, ignores quality, and penalises career gaps.
* **Career gaps:** gaps lower the years figure and can remove recent skills; a candidate returning from leave may be unfairly ranked down.
* **Fresh graduates:** short or no experience and fewer listed skills; projects and internships may not be captured by lexical matching.
* **Career changers:** transferable skills use different words, so TF-IDF/skill overlap under-scores them (the "terminology" failure mode above).
* **College reputation:** a proxy for socio-economic background, region and caste; it must not influence scores, and the education preference in job text is excluded from scoring.
* **Names, gender and age must never influence scores:** they carry no job-relevant information and invite discrimination.
* The ranking is a **decision-support tool**: a human must review candidates (especially resumes flagged as missing sections), and outcomes must be audited regularly.

## 8. API proposal
`POST /v1/resume/rank` accepts either a stored `job_id` or an inline job description, plus candidate resume texts; it returns ranked candidates, score components,
skill overlap, and an explanation. See [`docs/API_PROPOSAL.md`](docs/API_PROPOSAL.md) for request/response shapes and validation errors. It is a proposal only:
Task 11 does not implement a working HTTP endpoint. `ranking_engine.top_k_for_job` formats top results from an already-computed ranking.

## 9. Install and run
```
cd task11
python -m venv .venv && source .venv/bin/activate        # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/run_task11.py          # prints tables, writes reports/
python -m pytest -ra                  # test count and skipped-test summary shown by pytest
```
Optional overrides: `CORTEXHR_TASK11_DATA`, `CORTEXHR_TASK11_REPORTS`.

## 10. Outputs - `reports/`
`ranked_candidates.csv` (all 1,850 pairs, rank per job, explanation fields; human labels appended in `eval_only_*` columns, blank where unlabelled), `top5_per_job.csv`,
`ranking_quality.csv`, `ranking_quality_ablation.csv`, `tie_sensitivity.csv`, `misranking_analysis.csv`, `fairness_audit.csv`, `extraction_validation.csv`,
`dataset_inspection.json`, `run_summary.json`.

## 11. Limitations and future work
* Lexical matching: indirect skills ("deployed a model serving...") and abbreviations/synonyms outside the table are missed; broader terms over-credit ("Google Analytics" -> "Analytics").
* Resumes without a SKILLS section and some two-column layouts are under-scored (see fairness); add section-aware parsing and a manual-review flag.
* Small, synthetic data: 10 jobs, 185 resumes (160 originals + 25 bias twins that duplicate originals' content), 555 labels; metrics are indicative only. Twin resumes appear as separate candidates in the labelled pools. Unlabelled pairs cannot be evaluated.
* TF-IDF scale is small, so the nominal 60/40 split is not the effective split; consider calibrating, embeddings, or a title-family feature - validated on more data and re-audited.
* Company names are not scrubbed (not a protected attribute, but could proxy prestige).
* Text redaction is pattern-based: a name mention that is absent from the `candidate_name` field and lacks a name label, or an unknown institution phrased without an institution
  marker, may not be recognized. Production use requires dedicated PII detection and a human-reviewed redaction audit; current tests cover supplied fields and representative formats,
  not a universal privacy guarantee.
* Human labels may themselves be biased; they are a reference, not ground truth.
