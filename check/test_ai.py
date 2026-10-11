"""Перевірка матеріалів частини Б: pytest check -q (змінна AI_DIR задає іншу папку, TODAY_DATE задає дату перевірки)."""
import os
from pathlib import Path

import ai_rules as ar
import pytest

ROOT = Path(__file__).resolve().parent.parent
FOLDER = Path(os.environ.get("AI_DIR", ROOT / "my_ai"))
TODAY = os.environ.get("TODAY_DATE")


@pytest.fixture(scope="module")
def material():
    return ar.Material(FOLDER, TODAY)


@pytest.mark.parametrize("rule", ar.RULES, ids=lambda r: r.__name__)
def test_rule(material, rule):
    problems = rule(material)
    assert not problems, "; ".join(problems)
