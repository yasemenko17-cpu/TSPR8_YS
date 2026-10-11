"""Відкриті тести задачі 6: Класифікація завдань за правилами команди.

Запуск: pytest tests/test_variant_06.py
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

FUNC = "classify"
CASES = [
    ('T06-S1-1', ([{'id': 'Z-1',
   'personal_data': False,
   'anonymized': False,
   'secret_data': False,
   'decision': 'немає',
   'error_cost': 'низька',
   'reversible': True,
   'checkable': 'людиною'},
  {'id': 'Z-3',
   'personal_data': False,
   'anonymized': False,
   'secret_data': False,
   'decision': 'пріоритет',
   'error_cost': 'низька',
   'reversible': True,
   'checkable': 'людиною'}],), {'rows': [{'id': 'Z-1', 'zone': 'можна', 'rule': 'D1', 'checks': ['запис у журналі']},
          {'id': 'Z-3', 'zone': 'не можна', 'rule': 'N2', 'checks': []}],
 'counts': {'можна': 1, 'лише з перевіркою': 0, 'не можна': 1}}),
    ('T06-S2-1', ([{'id': 'Z-2',
   'personal_data': False,
   'anonymized': False,
   'secret_data': False,
   'decision': 'немає',
   'error_cost': 'висока',
   'reversible': False,
   'checkable': 'людиною'},
  {'id': 'Z-7',
   'personal_data': True,
   'anonymized': True,
   'secret_data': False,
   'decision': 'немає',
   'error_cost': 'низька',
   'reversible': True,
   'checkable': 'людиною'}],), {'rows': [{'id': 'Z-2',
           'zone': 'лише з перевіркою',
           'rule': 'V1',
           'checks': ['огляд людиною', 'друга людина', 'запис у журналі']},
          {'id': 'Z-7',
           'zone': 'лише з перевіркою',
           'rule': 'V4',
           'checks': ['огляд людиною', 'запис у журналі']}],
 'counts': {'можна': 0, 'лише з перевіркою': 2, 'не можна': 0}}),
    ('T06-S3-1', ([{'id': 'Z-5',
   'personal_data': False,
   'anonymized': False,
   'secret_data': False,
   'decision': 'немає',
   'error_cost': 'низька',
   'reversible': True,
   'checkable': 'ні'},
  {'id': 'Z-6',
   'personal_data': False,
   'anonymized': False,
   'secret_data': False,
   'decision': 'немає',
   'error_cost': 'висока',
   'reversible': True,
   'checkable': 'ні'}],), {'rows': [{'id': 'Z-5',
           'zone': 'лише з перевіркою',
           'rule': 'V5',
           'checks': ['огляд людиною', 'запис у журналі']},
          {'id': 'Z-6', 'zone': 'не можна', 'rule': 'N4', 'checks': []}],
 'counts': {'можна': 0, 'лише з перевіркою': 1, 'не можна': 1}}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_06(args, expected):
    check(6, FUNC, args, expected)
