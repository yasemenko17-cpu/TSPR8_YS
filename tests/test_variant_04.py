"""Відкриті тести задачі 4: Тести, що нічого не перевіряють.

Запуск: pytest tests/test_variant_04.py
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

FUNC = "weak_tests"
CASES = [
    ('T04-S1-1', ('import pytest\n\ndef test_a():\n    cancel(1)\n\ndef test_b():\n    assert cancel(1) == 2\n',), {'weak': [{'test': 'test_a', 'problems': ['немає перевірок']}], 'total': 2, 'share': 50.0}),
    ('T04-S2-1', ('def test_a():\n'
 '    assert price(2) is not None\n'
 '\n'
 'def test_b():\n'
 '    assert len(price(2)) >= 0\n'
 '\n'
 'def test_c():\n'
 '    assert price(2) == 60\n',), {'weak': [{'test': 'test_a', 'problems': ['слабка перевірка']},
          {'test': 'test_b', 'problems': ['завжди істинна']}],
 'total': 3,
 'share': 66.7}),
    ('T04-S3-1', ('import pytest\n'
 '\n'
 '@pytest.mark.skip(reason="пізніше")\n'
 'def test_a():\n'
 '    assert attach(5) == 5\n'
 '\n'
 'def test_b():\n'
 '    try:\n'
 '        assert attach(6) is None\n'
 '    except Exception:\n'
 '        pass\n',), {'weak': [{'test': 'test_a', 'problems': ['пропущено']},
          {'test': 'test_b', 'problems': ['виняток проковтнуто']}],
 'total': 2,
 'share': 100.0}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_04(args, expected):
    check(4, FUNC, args, expected)
