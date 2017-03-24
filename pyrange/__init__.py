# coding: utf-8

import operator
import re


pattern = r'([<>=]+)?(\d+(\.\d+)?)'
op = {
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    '=': operator.eq,
    'and': operator.and_,
    'or': operator.or_,
}


class BaseRange(object):
    _cast = None

    def __call__(self, value):
        self.value = value
        self._attr = [
            (k, v)
            for k, v in self.__class__.__dict__.items()
            if not k.startswith('_')]

        value = self.value
        cast = self.__class__._cast
        for k, v in self._attr:
            if cast:
                value = cast(value)

            res = v(value, k)
            if res:
                return res


class Field(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, value, field):
        return field if self.function(value) else None


class RangeField(object):
    def __init__(self, start, end=None, cond='and'):
        self.start = start
        self.end = end
        self.cond = op[cond]

    def __call__(self, value, field):
        start_groups = re.search(pattern, self.start).groups()
        start_operator_function = op[start_groups[0]]
        start_num = float(start_groups[1])

        if not self.end:
            return field if start_operator_function(float(value), start_num) else None

        end_groups = re.search(pattern, self.end).groups()
        end_operator_function = op[end_groups[0]]
        end_num = float(end_groups[1])
        if self.cond(start_operator_function(float(value), start_num), end_operator_function(float(value), end_num)):
            return field


class RangeOrField(RangeField):
    def __init__(self, start, end=None):
        super().__init__(start, end, 'or')