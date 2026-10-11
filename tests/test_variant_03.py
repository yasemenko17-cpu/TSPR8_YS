"""Відкриті тести задачі 3: Покриття критеріїв приймання тестами.

Запуск: pytest tests/test_variant_03.py
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

FUNC = "coverage"
CASES = [
    ('T03-S1-1', ([{'id': 'AC-1', 'boundary': 12}, {'id': 'AC-5', 'boundary': None}],
 [{'id': 'T-1', 'covers': ['AC-1'], 'value': 12, 'expect': 'ok'},
  {'id': 'T-2', 'covers': ['AC-1'], 'value': 13, 'expect': 'error'},
  {'id': 'T-8', 'covers': ['AC-5'], 'value': None, 'expect': 'ok'}]), {'rows': [{'id': 'AC-1', 'status': 'покрито', 'missing': []},
          {'id': 'AC-5', 'status': 'частково', 'missing': ['негативний тест']}],
 'covered_pct': 50.0,
 'unknown_claims': [],
 'orphans': []}),
    ('T03-S2-1', ([{'id': 'AC-2', 'boundary': 3}, {'id': 'AC-5', 'boundary': None}],
 [{'id': 'T-3', 'covers': ['AC-2'], 'value': 3, 'expect': 'ok'},
  {'id': 'T-4', 'covers': ['AC-2'], 'value': 4, 'expect': 'error'}]), {'rows': [{'id': 'AC-2', 'status': 'покрито', 'missing': []},
          {'id': 'AC-5', 'status': 'не покрито', 'missing': ['позитивний тест', 'негативний тест']}],
 'covered_pct': 50.0,
 'unknown_claims': [],
 'orphans': []}),
    ('T03-S3-1', ([{'id': 'AC-1', 'boundary': 5}, {'id': 'AC-2', 'boundary': 10}],
 [{'id': 'T-1', 'covers': ['AC-1'], 'value': 5, 'expect': 'ok'},
  {'id': 'T-3', 'covers': ['AC-2'], 'value': 10, 'expect': 'ok'}]), {'rows': [{'id': 'AC-1', 'status': 'частково', 'missing': ['значення 6 (error)']},
          {'id': 'AC-2', 'status': 'частково', 'missing': ['значення 11 (error)']}],
 'covered_pct': 0.0,
 'unknown_claims': [],
 'orphans': []}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_03(args, expected):
    check(3, FUNC, args, expected)
