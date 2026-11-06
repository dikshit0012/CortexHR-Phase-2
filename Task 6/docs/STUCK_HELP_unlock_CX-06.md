# CX-06 evaluation resource check

**Current status: resolved using the external official CSV; the workbook has no `unlock_CX-06` sheet.**

The current audit used the separate official `unlock_CX-06.csv`, located outside the repository and excluded from Git. The
workbook contains the `payroll_anomaly_labels` compatibility sheet, not the required `unlock_CX-06` worksheet. The Task 6
pipeline was explicitly run with `--labels <path-to-unlock_CX-06.csv>` after completing predictions. Its report records
`unlock_CX-06.csv` as the source and marks the run final.

## Verification

- `unlock_CX-06.csv`: 100 rows, 5 columns, 8 error types.
- The CSV label rows match `payroll_anomaly_labels` exactly.
- All 100 `payroll_item_id` values match feature rows; there are no duplicate or unmatched label keys.
- The end-to-end run uses the explicit CSV and emits no provisional-label warning.

For a fresh clone, obtain the CSV separately and pass `--labels <path>` or set `CORTEXHR_PAYROLL_LABELS`. If it is absent,
the compatibility sheet is a substitute and the report marks evaluation as provisional.
