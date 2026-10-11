"""Відкриті тести задачі 7: Метрики журналу використання.

Запуск: pytest tests/test_variant_07.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy

import pytest
from conftest import load


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


def check(number, func, args, expected):
    call = getattr(load(number), func)
    before = copy.deepcopy(args)
    if isinstance(expected, ValueError):
        with pytest.raises(ValueError) as info:
            call(*args)
        assert str(info.value) == str(expected)
    else:
        result = call(*args)
        assert norm(result) == norm(expected)
        assert type(result) is type(expected)
    assert args == before, "функція не повинна змінювати вхідні дані"

FUNC = "log_metrics"
CASES = [
    ('T07-S1-1', ([{'id': 'A-01',
   'date': '2026-09-14',
   'stage': 'історії',
   'tool': 'Асистент А',
   'request': 'Згенеруй чернетку за описом продукту і словником ролей',
   'data_class': 'вигадані',
   'outcome': 'правка',
   'minutes_ai': 18,
   'minutes_manual_est': 35,
   'defects_caught': 2,
   'defects_escaped': 0,
   'note': 'Правок немає, результат прийнято.'},
  {'id': 'A-02',
   'date': '2026-09-14',
   'stage': 'історії',
   'tool': 'Асистент А',
   'request': 'Згенеруй чернетку за описом продукту і словником ролей',
   'data_class': 'вигадані',
   'outcome': 'прийнято',
   'minutes_ai': 9,
   'minutes_manual_est': 20,
   'defects_caught': 0,
   'defects_escaped': 1,
   'note': 'Правок немає, результат прийнято.'},
  {'id': 'A-03',
   'date': '2026-09-16',
   'stage': 'тести',
   'tool': 'Асистент А',
   'request': 'Згенеруй чернетку за описом продукту і словником ролей',
   'data_class': 'вигадані',
   'outcome': 'відхилено',
   'minutes_ai': 15,
   'minutes_manual_est': 30,
   'defects_caught': 2,
   'defects_escaped': 0,
   'note': 'Правок немає, результат прийнято.'}],), {'total': 3,
 'shares': {'прийнято': 33.3, 'правка': 33.3, 'відхилено': 33.3},
 'used_pct': 66.7,
 'by_stage': {'історії': {'n': 2, 'accepted_pct': 50.0}, 'тести': {'n': 1, 'accepted_pct': 0.0}},
 'by_week': {'2026-W38': {'n': 3, 'accepted_pct': 33.3}},
 'defects': {'caught': 4, 'escaped': 1, 'caught_pct': 80.0},
 'time': {'ai': 42, 'manual': 85, 'saved': 43, 'saved_pct': 50.6},
 'flags': []}),
    ('T07-S2-1', ([{'id': 'B-01',
   'date': '2026-09-07',
   'stage': 'історії',
   'tool': 'Асистент А',
   'request': 'Згенеруй чернетку за описом продукту і словником ролей',
   'data_class': 'вигадані',
   'outcome': 'прийнято',
   'minutes_ai': 10,
   'minutes_manual_est': 30,
   'defects_caught': 0,
   'defects_escaped': 1,
   'note': 'Правок немає, результат прийнято.'},
  {'id': 'B-02',
   'date': '2026-09-08',
   'stage': 'історії',
   'tool': 'Асистент А',
   'request': 'Згенеруй чернетку за описом продукту і словником ролей',
   'data_class': 'вигадані',
   'outcome': 'прийнято',
   'minutes_ai': 8,
   'minutes_manual_est': 25,
   'defects_caught': 0,
   'defects_escaped': 0,
   'note': 'Правок немає, результат прийнято.'}],), {'total': 2,
 'shares': {'прийнято': 100.0, 'правка': 0.0, 'відхилено': 0.0},
 'used_pct': 100.0,
 'by_stage': {'історії': {'n': 2, 'accepted_pct': 100.0}},
 'by_week': {'2026-W37': {'n': 2, 'accepted_pct': 100.0}},
 'defects': {'caught': 0, 'escaped': 1, 'caught_pct': 0.0},
 'time': {'ai': 18, 'manual': 55, 'saved': 37, 'saved_pct': 67.3},
 'flags': ['можлива поверхнева перевірка']}),
    ('T07-S3-1', ([{'id': 'C-01',
   'date': '2026-09-28',
   'stage': 'історії',
   'tool': 'Асистент А',
   'request': 'Згенеруй чернетку за описом продукту і словником ролей',
   'data_class': 'вигадані',
   'outcome': 'відхилено',
   'minutes_ai': 15,
   'minutes_manual_est': 20,
   'defects_caught': 1,
   'defects_escaped': 0,
   'note': 'Правок немає, результат прийнято.'},
  {'id': 'C-03',
   'date': '2026-09-29',
   'stage': 'тести',
   'tool': 'Асистент А',
   'request': 'Згенеруй чернетку за описом продукту і словником ролей',
   'data_class': 'вигадані',
   'outcome': 'відхилено',
   'minutes_ai': 20,
   'minutes_manual_est': 25,
   'defects_caught': 2,
   'defects_escaped': 0,
   'note': 'Правок немає, результат прийнято.'}],), {'total': 2,
 'shares': {'прийнято': 0.0, 'правка': 0.0, 'відхилено': 100.0},
 'used_pct': 0.0,
 'by_stage': {'історії': {'n': 1, 'accepted_pct': 0.0}, 'тести': {'n': 1, 'accepted_pct': 0.0}},
 'by_week': {'2026-W40': {'n': 2, 'accepted_pct': 0.0}},
 'defects': {'caught': 3, 'escaped': 0, 'caught_pct': 100.0},
 'time': {'ai': 35, 'manual': 45, 'saved': 10, 'saved_pct': 22.2},
 'flags': ['асистент рідко допомагає']}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_07(args, expected):
    check(7, FUNC, args, expected)
