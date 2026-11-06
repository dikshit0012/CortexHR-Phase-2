import shutil
import sys
import warnings
from pathlib import Path

import pytest

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cortexhr_task14 import config  # noqa: E402


@pytest.fixture(scope="session")
def loaded():
    from cortexhr_task14.model_loader import load_attrition_v2
    return load_attrition_v2()


@pytest.fixture(scope="session")
def inputs(loaded):
    from cortexhr_task14.employee_scoring import build_scoring_inputs
    return build_scoring_inputs(loaded)


@pytest.fixture(scope="session")
def result(tmp_path_factory):
    """Full pipeline on the real data. Reuses cached REAL SHAP values from reports/internal when present (computing them takes ~12 min)."""
    from cortexhr_task14.pipeline import run
    out = tmp_path_factory.mktemp("reports14")
    cache = config.TASK14_ROOT / "reports" / "internal"
    if (cache / "shap_values.csv").exists():
        (out / "internal").mkdir()
        for f in ("shap_values.csv", "shap_values.meta.json"):
            shutil.copy(cache / f, out / "internal" / f)
    return run(reports_dir=out, stability_check=False, progress=False) | {"dir": out}
