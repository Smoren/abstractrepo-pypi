import abc
from enum import Enum
from typing import List, Tuple


class OrderDirection(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class OrderParam:
    attribute: str
    direction: OrderDirection = OrderDirection.ASC

    def __init__(self, attribute: str, direction: OrderDirection):
        self.attribute = attribute
        self.direction = direction


class OrderParams:
    params: List[OrderParam]

    def __init__(self, *params: OrderParam):
        self.params = list(params)


class OrderParamsBuilder:
    _params: List[OrderParam]

    def __init__(self):
        self._params = []

    def add(self, attribute: str, direction: OrderDirection = OrderDirection.ASC) -> "OrderParamsBuilder":
        self._params.append(OrderParam(attribute, direction))
        return self

    def add_mass(self, *items: Tuple[str, OrderDirection]) -> "OrderParamsBuilder":
        for item in items:
            self.add(*item)
        return self

    def build(self) -> OrderParams:
        return OrderParams(*self._params)


class OrderParamsConverterInterface(abc.ABC):
    @abc.abstractmethod
    def convert(self, order: OrderParams) -> OrderParams:
        raise NotImplementedError()
