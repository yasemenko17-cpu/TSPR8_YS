"""Відкриті тести задачі 9: Брама Definition of Done для змін із ШІ.

Запуск: pytest tests/test_variant_09.py
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

FUNC = "gate"
CASES = [
    ('T09-S1-1', ([{'id': 'PR-1',
   'title': 'Скасування запису',
   'ai_used': True,
   'zone': 'лише з перевіркою',
   'author': 'Андрій',
   'reviewer': 'Марія',
   'lines': 120,
   'tests_added': 3,
   'tests_pass': True,
   'secrets_scan': True,
   'log_entry': 'A-03'},
  {'id': 'PR-3',
   'title': 'Правила знижок',
   'ai_used': True,
   'zone': 'не можна',
   'author': 'Андрій',
   'reviewer': 'Марія',
   'lines': 80,
   'tests_added': 1,
   'tests_pass': True,
   'secrets_scan': True,
   'log_entry': 'A-05'}],
 ['A-01', 'A-02', 'A-03', 'A-04', 'A-05', 'A-06', 'A-07', 'A-08']), {'rows': [{'id': 'PR-1', 'decision': 'прийнято', 'fails': [], 'sample': True},
          {'id': 'PR-3',
           'decision': 'відхилено',
           'fails': ['завдання із зони «не можна» не можна віддавати асистентові'],
           'sample': False}],
 'counts': {'прийнято': 1, 'повернуто': 0, 'відхилено': 1}}),
    ('T09-S2-1', ([{'id': 'PR-2',
   'title': 'Журнал оплат',
   'ai_used': True,
   'zone': 'лише з перевіркою',
   'author': 'Леся',
   'reviewer': 'Тарас',
   'lines': 280,
   'tests_added': 1,
   'tests_pass': True,
   'secrets_scan': True,
   'log_entry': 'B-09'},
  {'id': 'PR-4',
   'title': 'Статус броні',
   'ai_used': False,
   'zone': None,
   'author': 'Леся',
   'reviewer': 'Тарас',
   'lines': 640,
   'tests_added': 2,
   'tests_pass': True,
   'secrets_scan': True,
   'log_entry': None}],
 ['B-01', 'B-02', 'B-03', 'B-04', 'B-05', 'B-06', 'B-07']), {'rows': [{'id': 'PR-2', 'decision': 'повернуто', 'fails': ['запису B-09 немає в журналі'], 'sample': False},
          {'id': 'PR-4',
           'decision': 'повернуто',
           'fails': ['зміна завелика (640 рядків, ліміт 600)'],
           'sample': False}],
 'counts': {'прийнято': 0, 'повернуто': 2, 'відхилено': 0}}),
    ('T09-S3-1', ([{'id': 'PR-3',
   'title': 'Звіт за тиждень',
   'ai_used': True,
   'zone': 'лише з перевіркою',
   'author': 'Остап',
   'reviewer': '',
   'lines': 150,
   'tests_added': 1,
   'tests_pass': True,
   'secrets_scan': True,
   'log_entry': 'C-02'},
  {'id': 'PR-6',
   'title': 'Фільтр заявок',
   'ai_used': True,
   'zone': 'лише з перевіркою',
   'author': 'Ірма',
   'reviewer': 'Остап',
   'lines': 90,
   'tests_added': 0,
   'tests_pass': True,
   'secrets_scan': True,
   'log_entry': None}],
 ['C-01', 'C-02', 'C-03', 'C-04', 'C-05', 'C-06']), {'rows': [{'id': 'PR-3', 'decision': 'повернуто', 'fails': ['немає рецензента'], 'sample': False},
          {'id': 'PR-6',
           'decision': 'повернуто',
           'fails': ['не вказано запис журналу', 'немає нового тесту'],
           'sample': False}],
 'counts': {'прийнято': 0, 'повернуто': 2, 'відхилено': 0}}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_09(args, expected):
    check(9, FUNC, args, expected)
