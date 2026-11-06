import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cortexhr_task11 import paths  # noqa: E402
from cortexhr_task11.pipeline import run  # noqa: E402


@pytest.fixture(scope="session")
def reports_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("reports")


@pytest.fixture(scope="session")
def result(reports_dir):
    """One real run on the supplied data; reports are written to a temp folder (the committed reports/ are untouched)."""
    return run(paths.DATA_DIR, reports_dir, write=True)


@pytest.fixture()
def data_copy(tmp_path):
    d = tmp_path / "data"
    shutil.copytree(paths.DATA_DIR, d)
    return d
