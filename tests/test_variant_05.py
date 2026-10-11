"""Відкриті тести задачі 5: Знеособлення даних перед надсиланням.

Запуск: pytest tests/test_variant_05.py
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

FUNC = "anonymize"
CASES = [
    ('T05-S1-1', ('Ірина Коваль написала на irina.koval@example.com. Олег Бондар відповів Ірині Коваль.',
 [['Ірина Коваль', 'Ірині Коваль', 'Ірини Коваль'], ['Олег Бондар', 'Олега Бондаря']]), {'blocked': False,
 'reasons': [],
 'text': '[ОСОБА_1] написала на [EMAIL_1]. [ОСОБА_2] відповів [ОСОБА_1].',
 'mapping': {'[ОСОБА_1]': 'Ірина Коваль', '[EMAIL_1]': 'irina.koval@example.com', '[ОСОБА_2]': 'Олег Бондар'},
 'counts': {'ОСОБА': 2, 'EMAIL': 1}}),
    ('T05-S2-1', ('Дзвінок 0671112233 і +380 67 111 22 33 від Петра Шевчука.',
 [['Петро Шевчук', 'Петру Шевчуку', 'Петра Шевчука'], ['Ганна Мельник', 'Ганні Мельник']]), {'blocked': False,
 'reasons': [],
 'text': 'Дзвінок [ТЕЛЕФОН_1] і [ТЕЛЕФОН_1] від [ОСОБА_1].',
 'mapping': {'[ТЕЛЕФОН_1]': '0671112233', '[ОСОБА_1]': 'Петра Шевчука'},
 'counts': {'ТЕЛЕФОН': 1, 'ОСОБА': 1}}),
    ('T05-S3-1', ('sk-abcdefghijklmnop1234 пароль: qwerty',
 [['Оксана Лисенко', 'Оксані Лисенко', 'Оксану Лисенко'], ['Василь Гнатюк', 'Василя Гнатюка']]), {'blocked': True, 'reasons': ['ключ API', 'пароль'], 'text': None, 'mapping': {}, 'counts': {}}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_05(args, expected):
    check(5, FUNC, args, expected)
