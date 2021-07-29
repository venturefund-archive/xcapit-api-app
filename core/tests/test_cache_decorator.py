from functools import lru_cache as cache


class TestCache:
    def __init__(self, count: int):
        self._count = count

    @cache
    def sum(self, amount: int = 1):
        self._count += amount
        return self._count

    @property
    def count(self):
        return self._count


def test_cache_decorator():
    obj = TestCache(1)
    assert obj.sum() == 2
    assert obj.count == 2
    assert obj.sum() == 2
    assert obj.count == 2
    assert obj.sum(1) == 3
    assert obj.count == 3
    assert obj.sum(1) == 3
    assert obj.count == 3
    assert obj.sum() == 2
    assert obj.count == 3
    assert obj.sum(2) == 5
    assert obj.count == 5


def test_cache_decorator_different_objects():
    obj_1 = TestCache(1)
    obj_2 = TestCache(2)
    assert obj_1.sum() == 2
    assert obj_1.count == 2
    assert obj_1.sum() == 2
    assert obj_1.count == 2
    assert obj_2.sum() == 3
    assert obj_2.count == 3
    assert obj_2.sum() == 3
    assert obj_2.count == 3
