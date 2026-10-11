"""Відкриті тести задачі 10: Зведений звіт за спринт.

Запуск: pytest tests/test_variant_10.py
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

FUNC = "sprint_report"
CASES = [
    ('T10-S1-1', ({'stories': {'прийняти': 1, 'доопрацювати': 3, 'відхилити': 2},
  'requirements': {'підтверджена': 3, 'суперечить': 3, 'вигадана': 2},
  'coverage_pct': 40.0,
  'weak': {'weak': 6, 'total': 8},
  'log': {'caught': 9, 'escaped': 2},
  'gate': {'прийнято': 2, 'повернуто': 3, 'відхилено': 1}},), {'indicators': [{'name': 'Відхилені чернетки історій, %', 'value': 33.3, 'status': 'жовтий'},
                {'name': 'Вигадані й суперечливі вимоги, %', 'value': 62.5, 'status': 'червоний'},
                {'name': 'Покриття критеріїв, %', 'value': 40.0, 'status': 'червоний'},
                {'name': 'Слабкі тести, %', 'value': 75.0, 'status': 'червоний'},
                {'name': 'Дефекти, що прослизнули', 'value': 2, 'status': 'жовтий'},
                {'name': 'Зміни, повернуті або відхилені, %', 'value': 66.7, 'status': 'червоний'}],
 'counts': {'зелений': 0, 'жовтий': 2, 'червоний': 4},
 'decision': 'зупинити',
 'actions': ['уточнити запит: додати словник ролей і межі продукту',
             'заборонити приймати вимоги від асистента без звірки з описом',
             'не приймати набір тестів, доки не покрито кожен критерій',
             'не зараховувати тести, у яких немає справжньої перевірки',
             'розібрати прослизнулі дефекти на ретроспективі',
             'розібрати причини повернень і змінити процес']}),
    ('T10-S2-1', ({'stories': {'прийняти': 6, 'доопрацювати': 2, 'відхилити': 0},
  'requirements': {'підтверджена': 8, 'суперечить': 0, 'вигадана': 0},
  'coverage_pct': 95.0,
  'weak': {'weak': 0, 'total': 6},
  'log': {'caught': 4, 'escaped': 0},
  'gate': {'прийнято': 7, 'повернуто': 1, 'відхилено': 0}},), {'indicators': [{'name': 'Відхилені чернетки історій, %', 'value': 0.0, 'status': 'зелений'},
                {'name': 'Вигадані й суперечливі вимоги, %', 'value': 0.0, 'status': 'зелений'},
                {'name': 'Покриття критеріїв, %', 'value': 95.0, 'status': 'зелений'},
                {'name': 'Слабкі тести, %', 'value': 0.0, 'status': 'зелений'},
                {'name': 'Дефекти, що прослизнули', 'value': 0, 'status': 'зелений'},
                {'name': 'Зміни, повернуті або відхилені, %', 'value': 12.5, 'status': 'зелений'}],
 'counts': {'зелений': 6, 'жовтий': 0, 'червоний': 0},
 'decision': 'продовжувати',
 'actions': []}),
    ('T10-S3-1', ({'stories': {'прийняти': 4, 'доопрацювати': 1, 'відхилити': 1},
  'requirements': {'підтверджена': 5, 'суперечить': 0, 'вигадана': 0},
  'coverage_pct': 65.0,
  'weak': {'weak': 0, 'total': 5},
  'log': {'caught': 4, 'escaped': 0},
  'gate': {'прийнято': 5, 'повернуто': 1, 'відхилено': 0}},), {'indicators': [{'name': 'Відхилені чернетки історій, %', 'value': 16.7, 'status': 'зелений'},
                {'name': 'Вигадані й суперечливі вимоги, %', 'value': 0.0, 'status': 'зелений'},
                {'name': 'Покриття критеріїв, %', 'value': 65.0, 'status': 'червоний'},
                {'name': 'Слабкі тести, %', 'value': 0.0, 'status': 'зелений'},
                {'name': 'Дефекти, що прослизнули', 'value': 0, 'status': 'зелений'},
                {'name': 'Зміни, повернуті або відхилені, %', 'value': 16.7, 'status': 'зелений'}],
 'counts': {'зелений': 5, 'жовтий': 0, 'червоний': 1},
 'decision': 'посилити перевірку',
 'actions': ['не приймати набір тестів, доки не покрито кожен критерій']}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_10(args, expected):
    check(10, FUNC, args, expected)
