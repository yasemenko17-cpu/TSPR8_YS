"""Відкриті тести задачі 8: Перевірка запису журналу на повноту.

Запуск: pytest tests/test_variant_08.py
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

FUNC = "check_log"
CASES = [
    ('T08-S1-1', ([{'id': 'A-01',
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
   'note': 'Виправлено роль і прибрано вигадану знижку.'},
  {'id': 'A-02',
   'date': '2026-09-15',
   'stage': 'тести',
   'tool': 'Асистент А',
   'request': 'Згенеруй чернетку за описом продукту і словником ролей',
   'data_class': 'вигадані',
   'outcome': 'прийнято',
   'minutes_ai': 9,
   'minutes_manual_est': 20,
   'defects_caught': 1,
   'defects_escaped': 0,
   'note': 'Правок немає, результат прийнято.'}],
 '2026-10-05'), {'rows': [{'id': 'A-01', 'problems': []},
          {'id': 'A-02', 'problems': ['знайдено дефекти, але результат прийнято без змін']}],
 'ok': 1,
 'bad': 1,
 'complete': False}),
    ('T08-S2-1', ([{'id': 'B-01',
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
  {'id': 'B-03',
   'date': '2026-09-09',
   'stage': 'оцінки',
   'tool': 'Асистент Б',
   'request': 'Оціни складність історій у балах Fibonacci',
   'data_class': 'вигадані',
   'outcome': 'прийнято',
   'minutes_ai': 'десять',
   'minutes_manual_est': 20,
   'defects_caught': 0,
   'defects_escaped': 0,
   'note': 'Прийнято.'}],
 '2026-10-05'), {'rows': [{'id': 'B-01', 'problems': []}, {'id': 'B-03', 'problems': ['хвилини з ШІ мають бути додатними']}],
 'ok': 1,
 'bad': 1,
 'complete': False}),
    ('T08-S3-1', ([{'id': 'C-05',
   'date': '2026-10-01',
   'stage': 'оцінки',
   'request': 'Оціни складність цих історій за шкалою Fibonacci',
   'data_class': 'секретні',
   'outcome': 'відхилено',
   'minutes_ai': 10,
   'minutes_manual_est': 8,
   'defects_caught': 0,
   'defects_escaped': 0,
   'note': 'Оцінка не враховує складність.'}],
 '2026-10-05'), {'rows': [{'id': 'C-05', 'problems': ['немає поля tool', 'заборонений клас даних «секретні»']}],
 'ok': 0,
 'bad': 1,
 'complete': False}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_08(args, expected):
    check(8, FUNC, args, expected)
