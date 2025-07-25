import abc
from enum import Enum
from typing import List, Tuple


class OrderDirection(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class OrderOption:
    attribute: str
    direction: OrderDirection = OrderDirection.ASC

    def __init__(self, attribute: str, direction: OrderDirection):
        self.attribute = attribute
        self.direction = direction


class OrderOptions:
    params: List[OrderOption]

    def __init__(self, *params: OrderOption):
        self.params = list(params)


class OrderOptionsBuilder:
    _params: List[OrderOption]

    def __init__(self):
        self._params = []

    def add(self, attribute: str, direction: OrderDirection = OrderDirection.ASC) -> "OrderOptionsBuilder":
        self._params.append(OrderOption(attribute, direction))
        return self

    def add_mass(self, *items: Tuple[str, OrderDirection]) -> "OrderOptionsBuilder":
        for item in items:
            self.add(*item)
        return self

    def build(self) -> OrderOptions:
        return OrderOptions(*self._params)


class OrderOptionsConverterInterface(abc.ABC):
    @abc.abstractmethod
    def convert(self, order: OrderOptions) -> OrderOptions:
        raise NotImplementedError()
