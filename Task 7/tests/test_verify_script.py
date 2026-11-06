"""The independent verifier must accept a correct run and reject tampering."""
import importlib.util
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pytest

from test_task7_pipeline_smoke import load_runner, write_workbook

VERIFY = Path(__file__).resolve().parents[1] / "scripts" / "verify_task7_reports.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("verify_task7_reports", VERIFY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def run(tmp_path, planted_panel, planted_attendance):
    wb = write_workbook(tmp_path / "wb.xlsx", planted_panel[0], planted_attendance[0])
    out = tmp_path / "reports"
    load_runner().main(["--workbook", str(wb), "--reports-dir", str(out)])
    return wb, out


def test_verifier_accepts_a_correct_run(run):
    wb, out = run
    assert load_verifier().verify(out, wb) == []


def test_verifier_cli_reports_successful_reconciliation(run):
    wb, out = run
    result = subprocess.run(
        [sys.executable, str(VERIFY), str(out), str(wb)],
        capture_output=True, text=True, check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert f"OK: outputs in {out}" in result.stdout


def test_duplicate_amount_reconciliation_separates_groups_within_employee_month():
    verifier = load_verifier()
    raw = pd.DataFrame([
        {"payroll_item_id": "P1", "employee_id": "E1", "month": "2025-05-01", "gross_pay": 100,
         "total_deductions": 20, "net_pay": 80, "monthly_fixed_gross": 100, "payable_days": 31,
         "overtime_pay": 0, "variable_pay": 0, "pf_employee": 0, "role_id": "R1"},
        {"payroll_item_id": "P2", "employee_id": "E1", "month": "2025-05-01", "gross_pay": 100,
         "total_deductions": 20, "net_pay": 80, "monthly_fixed_gross": 100, "payable_days": 31,
         "overtime_pay": 0, "variable_pay": 0, "pf_employee": 0, "role_id": "R1"},
        {"payroll_item_id": "P3", "employee_id": "E1", "month": "2025-05-01", "gross_pay": 200,
         "total_deductions": 40, "net_pay": 160, "monthly_fixed_gross": 200, "payable_days": 31,
         "overtime_pay": 0, "variable_pay": 0, "pf_employee": 0, "role_id": "R1"},
        {"payroll_item_id": "P4", "employee_id": "E1", "month": "2025-05-01", "gross_pay": 200,
         "total_deductions": 40, "net_pay": 160, "monthly_fixed_gross": 200, "payable_days": 31,
         "overtime_pay": 0, "variable_pay": 0, "pf_employee": 0, "role_id": "R1"},
    ])
    official = pd.DataFrame([
        {"source_dataset": "payroll_monthly_features", "record_id": f"P{i}", "employee_id": "E1",
         "period": "2025-05-01", "reason_code": "DUPLICATE_PAYMENT"}
        for i in range(1, 5)
    ])

    amounts = verifier.expected_amounts(raw, official)

    assert amounts.to_dict() == {"P1": 40.0, "P2": 40.0, "P3": 80.0, "P4": 80.0}


def test_role_outlier_amount_reconciliation_uses_previous_month_role_median():
    verifier = load_verifier()
    raw = pd.DataFrame([
        {"payroll_item_id": "P1", "employee_id": "E1", "month": "2025-04-01", "gross_pay": 100,
         "total_deductions": 20, "net_pay": 80, "monthly_fixed_gross": 100, "payable_days": 30,
         "overtime_pay": 0, "variable_pay": 0, "pf_employee": 0, "role_id": "R1"},
        {"payroll_item_id": "P2", "employee_id": "E2", "month": "2025-04-01", "gross_pay": 200,
         "total_deductions": 40, "net_pay": 160, "monthly_fixed_gross": 200, "payable_days": 30,
         "overtime_pay": 0, "variable_pay": 0, "pf_employee": 0, "role_id": "R1"},
        {"payroll_item_id": "P3", "employee_id": "E3", "month": "2025-05-01", "gross_pay": 300,
         "total_deductions": 60, "net_pay": 240, "monthly_fixed_gross": 300, "payable_days": 31,
         "overtime_pay": 0, "variable_pay": 0, "pf_employee": 0, "role_id": "R1"},
    ])
    official = pd.DataFrame([{
        "source_dataset": "payroll_monthly_features", "record_id": "P3", "employee_id": "E3",
        "period": "2025-05-01", "reason_code": "PAY_ABOVE_ROLE_NORM",
    }])

    amounts = verifier.expected_amounts(raw, official)

    assert amounts.to_dict() == {"P3": 150.0}


def _edit(out, fn):
    path = out / "task7_anomaly_results.csv"
    df = pd.read_csv(path)
    fn(df)
    df.to_csv(path, index=False)


@pytest.mark.parametrize("name,tamper,expected", [
    ("wrong amount", lambda d: d.__setitem__("money_at_risk", d["money_at_risk"].where(d.index != 0, d["money_at_risk"] + 500)), "differ from the independent recomputation"),
    ("wrong column order", lambda d: d.insert(0, "record_id", d.pop("record_id")), "columns differ"),
    ("unknown reason code", lambda d: d.__setitem__("reason_code", d["reason_code"].where(d.index != 0, "MADE_UP")), "unknown reason codes"),
    ("empty text", lambda d: d.__setitem__("reason_text", d["reason_text"].where(d.index != 0, "")), "empty reason_text"),
    ("invented record", lambda d: d.__setitem__("record_id", d["record_id"].where(d.index != 0, "PI-NOT-REAL")), "not in source"),
    ("wrong employee", lambda d: d.__setitem__("employee_id", d["employee_id"].where(d.index != 0, "E-WRONG")), "employee_id mismatch"),
    ("broken ranking", lambda d: d.__setitem__("money_at_risk", d["money_at_risk"].iloc[::-1].to_numpy()), "not ranked"),
])
def test_verifier_rejects_tampering(run, name, tamper, expected):
    wb, out = run
    _edit(out, tamper)
    problems = load_verifier().verify(out, wb)
    assert any(expected in p for p in problems), (name, problems)


def test_verifier_rejects_a_sample_that_is_not_part_of_the_output(run):
    wb, out = run
    path = out / "task7_sample_20_flags.csv"
    s = pd.read_csv(path)
    s.loc[0, "result_id"] = "AN-9999"
    s.to_csv(path, index=False)
    assert any("not in the official output" in p for p in load_verifier().verify(out, wb))
