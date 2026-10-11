import pytest
from conftest import load

M = load(8)  # Номер вашої задачі (Задача 8)

@pytest.mark.parametrize("args, expected", [
    (
        ([
            {
                "id": "B-01",
                "date": "2026-09-07",
                "stage": "історії",
                "tool": "Асистент Б",
                "request": "Згенеруй чернетку історії за описом",
                "data_class": "вигадані",
                "outcome": "прийнято",
                "minutes_ai": 10,
                "minutes_manual_est": 30,
                "defects_caught": 0,
                "defects_escaped": 1,
                "note": "Прийнято без змін."
            }
        ], "2026-10-05"),
        {
            "rows": [{"id": "B-01", "problems": []}],
            "ok": 1,
            "bad": 0,
            "complete": True
        }
    ),
])
def test_my_cases(args, expected):
    assert M.check_log(*args) == expected