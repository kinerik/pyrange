# coding: utf-8

import pytest

import pyrange


class RangeExample(pyrange.BaseRange):
    true = pyrange.Field(lambda x: x % 2 == 0)
    false = pyrange.Field(lambda x: x % 2 != 0)


@pytest.fixture
def range_obj():
    return RangeExample()


def test_simple_range(range_obj):
    assert range_obj(0) == 'true'
    assert range_obj(1) == 'false'
    assert range_obj(2) == 'true'
    assert range_obj(3) == 'false'
    assert range_obj(4) == 'true'
