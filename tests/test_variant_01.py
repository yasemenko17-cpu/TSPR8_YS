"""Відкриті тести задачі 1: Оцінка чернетки історії за правилами якості.

Запуск: pytest tests/test_variant_01.py
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

FUNC = "rate_story"
CASES = [
    ('T01-S1-1', ({'id': 'D-4',
  'text': 'Як тренер, я хочу натиснути кнопку «Присутній» у таблиці, щоб відзначити присутність учасників.',
  'criteria': ['к1', 'к2']},
 {'roles': ['учасник', 'тренер', 'адміністратор клубу'],
  'solution_words': ['sql', 'api', 'json', 'кнопк', 'таблиц', 'базі даних', 'базу даних']}), {'id': 'D-4', 'score': 80, 'failed': ['Q4'], 'verdict': 'доопрацювати'}),
    ('T01-S2-1', ({'id': 'D-2',
  'text': 'Як гість, я хочу оплатити парковку без реєстрації, щоб заощадити час.',
  'criteria': ['к1', 'к2']},
 {'roles': ['водій', 'оператор', 'власник паркінгу'],
  'solution_words': ['sql', 'api', 'json', 'кнопк', 'таблиц', 'push', 'базі даних']}), {'id': 'D-2', 'score': 80, 'failed': ['Q2'], 'verdict': 'відхилити'}),
    ('T01-S3-1', ({'id': 'D-2', 'text': 'Як технік, я хочу бачити нові заявки, щоб бачити нові заявки.', 'criteria': ['к1']},
 {'roles': ['працівник', 'технік', 'керівник служби'],
  'solution_words': ['sql', 'api', 'json', 'кнопк', 'таблиц', 'базі даних', 'чат-бот']}), {'id': 'D-2', 'score': 60, 'failed': ['Q3', 'Q5'], 'verdict': 'доопрацювати'}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_01(args, expected):
    check(1, FUNC, args, expected)
