import abc
from enum import Enum
from typing import List, Tuple, Union


class OrderDirection(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class NonesOrder(Enum):
    FIRST = 'FIRST'
    LAST = 'LAST'


OrderOptionsTuple = Union[Tuple[str], Tuple[str, OrderDirection], Tuple[str, OrderDirection, NonesOrder]]


class OrderOption:
    attribute: str
    direction: OrderDirection
    nones: NonesOrder

    def __init__(self, attribute: str, direction: OrderDirection, nones: NonesOrder = NonesOrder.FIRST):
        self.attribute = attribute
        self.direction = direction
        self.nones = nones


class OrderOptions:
    _options: List[OrderOption]

    def __init__(self, *options: OrderOption):
        self._options = list(options)

    @property
    def options(self):
        return self._options


class OrderOptionsBuilder:
    _options: List[OrderOption]

    def __init__(self):
        self._options = []

    def add(self, attribute: str, direction: OrderDirection = OrderDirection.ASC, nones: NonesOrder = NonesOrder.LAST) -> "OrderOptionsBuilder":
        self._options.append(OrderOption(attribute, direction, nones))
        return self

    def add_mass(self, *items: OrderOptionsTuple) -> "OrderOptionsBuilder":
        for item in items:
            self.add(*item)
        return self

    def build(self) -> OrderOptions:
        return OrderOptions(*self._options)


class OrderOptionsConverterInterface(abc.ABC):
    @abc.abstractmethod
    def convert(self, order: OrderOptions) -> OrderOptions:
        raise NotImplementedError()
