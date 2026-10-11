"""Відкриті тести задачі 2: Пошук вигаданих і суперечливих вимог.

Запуск: pytest tests/test_variant_02.py
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

FUNC = "check_requirements"
CASES = [
    ('T02-S1-1', ({'facts': [{'stem': 'місц', 'value': 12, 'unit': 'місце'},
            {'stem': 'скасув', 'value': 3, 'unit': 'год'},
            {'stem': 'абонемент', 'value': 8, 'unit': 'заняття'},
            {'stem': 'заморож', 'value': 14, 'unit': 'доб'},
            {'stem': 'очікуван', 'value': 5, 'unit': 'особа'},
            {'stem': 'нагадуван', 'value': 2, 'unit': 'год'}],
  'features': ['розклад', 'присутн', 'запис', 'тренер', 'адміністратор']},
 [{'id': 'R-2', 'text': 'Скасувати запис можна за 180 хвилин до початку без списання заняття.'},
  {'id': 'R-3', 'text': 'Скасувати запис без списання можна не пізніше ніж за 2 години до початку.'}]), {'rows': [{'id': 'R-2', 'verdict': 'підтверджена', 'reason': 'збігається з описом'},
          {'id': 'R-3', 'verdict': 'суперечить', 'reason': 'у вимозі 120, в описі 180 (хв)'}],
 'counts': {'підтверджена': 1, 'суперечить': 1, 'вигадана': 0}}),
    ('T02-S2-1', ({'facts': [{'stem': 'діє', 'value': 24, 'unit': 'год'},
            {'stem': 'вартіст', 'value': 30, 'unit': 'грн'},
            {'stem': 'активн', 'value': 3, 'unit': 'бронь'},
            {'stem': 'пільгов', 'value': 10, 'unit': 'хв'},
            {'stem': 'повернен', 'value': 30, 'unit': 'хв'}],
  'features': ['завантаженість', 'завантаженост', 'тариф', 'водій', 'оператор', 'власник']},
 [{'id': 'R-5', 'text': 'Повернення коштів можливе за скасування за 1 годину до початку.'},
  {'id': 'R-6', 'text': 'Застосунок підтримує оплату криптовалютою.'}]), {'rows': [{'id': 'R-5', 'verdict': 'суперечить', 'reason': 'у вимозі 60, в описі 30 (хв)'},
          {'id': 'R-6', 'verdict': 'вигадана', 'reason': 'тема відсутня в описі'}],
 'counts': {'підтверджена': 0, 'суперечить': 1, 'вигадана': 1}}),
    ('T02-S3-1', ({'facts': [{'stem': 'критичн', 'value': 4, 'unit': 'год'},
            {'stem': 'файл', 'value': 5, 'unit': 'файл'},
            {'stem': 'розмір', 'value': 10, 'unit': 'мб'},
            {'stem': 'закрива', 'value': 7, 'unit': 'доб'}],
  'features': ['оцінк', 'звіт', 'технік', 'призначає', 'працівник']},
 [{'id': 'R-2', 'text': 'До заявки можна додати 10 файлів.'},
  {'id': 'R-5', 'text': 'Заявка закривається автоматично через 3 доби без відповіді.'}]), {'rows': [{'id': 'R-2', 'verdict': 'суперечить', 'reason': 'у вимозі 10, в описі 5 (файл)'},
          {'id': 'R-5', 'verdict': 'суперечить', 'reason': 'у вимозі 4320, в описі 10080 (хв)'}],
 'counts': {'підтверджена': 0, 'суперечить': 2, 'вигадана': 0}}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_02(args, expected):
    check(2, FUNC, args, expected)
