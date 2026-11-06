"""Task 10 router adapter; reuse the Task 9 chat model already loaded by this app."""
from __future__ import annotations

import sys
from pathlib import Path

from ._paths import REPO_ROOT

TASK10_SRC = str(REPO_ROOT / "task 10" / "src")
if TASK10_SRC not in sys.path:
    sys.path.insert(0, TASK10_SRC)

from cortexhr_task10.api import attach, router
from cortexhr_task10.classifier import Task9Classifier
from cortexhr_task10.config import Settings


def attach_converse(app) -> None:
    chat = getattr(app.state, "chat", None)
    if chat is None:
        app.state.converse = None
        app.state.demo_users = None
        return
    attach(app, Settings.from_env(), classifier=Task9Classifier(chat))


def converse_router():
    return router
