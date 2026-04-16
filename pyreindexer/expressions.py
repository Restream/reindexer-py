from enum import Enum, IntEnum
from typing import List, Union

from pyreindexer.constants import ValueType


class ExpressionType(IntEnum):
    Field = 0
    Values = 1
    Expression = 2
    SubQuery = 3


class FunctionType(IntEnum):
    FlatArrayLen = 0
    Now = 1


class TimeUnit(str, Enum):
    SEC = "sec"
    MSEC = "msec"
    USEC = "usec"
    NSEC = "nsec"

    def __str__(self):
        return self.value


class Expression:
    def _serialize(self) -> tuple[int, list]:
        raise NotImplementedError


class Field(Expression):
    def __init__(self, name: str):
        self.name = name

    def _serialize(self) -> tuple[int, list]:
        return ExpressionType.Field, [self.name]


class Values(Expression):
    def __init__(self, values: Union[ValueType, List[ValueType]]):
        self.values = values if isinstance(values, list) else [values]

    def _serialize(self) -> tuple[int, list]:
        return ExpressionType.Values, self.values


class SubQuery(Expression):
    def __init__(self, query):
        self.query = query

    def _serialize(self) -> tuple[int, list]:
        return ExpressionType.SubQuery, [self.query.query_wrapper_ptr]


class FlatArrayLen(Expression):
    def __init__(self, field: str):
        self.field = field

    def _serialize(self) -> tuple[int, list]:
        return ExpressionType.Expression, [[self.field], [], FunctionType.FlatArrayLen]


class Now(Expression):
    def __init__(self, time_unit: TimeUnit = TimeUnit.SEC):
        self.time_unit = time_unit.value

    def _serialize(self) -> tuple[int, list]:
        return ExpressionType.Expression, [[], [self.time_unit], FunctionType.Now]
