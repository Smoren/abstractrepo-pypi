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
    nones_order: NonesOrder

    def __init__(self, attribute: str, direction: OrderDirection, nones_order: NonesOrder = NonesOrder.FIRST):
        self.attribute = attribute
        self.direction = direction
        self.nones_order = nones_order


class OrderOptions:
    params: List[OrderOption]

    def __init__(self, *params: OrderOption):
        self.params = list(params)


class OrderOptionsBuilder:
    _params: List[OrderOption]

    def __init__(self):
        self._params = []

    def add(self, attribute: str, direction: OrderDirection = OrderDirection.ASC, nones_order: NonesOrder = NonesOrder.LAST) -> "OrderOptionsBuilder":
        self._params.append(OrderOption(attribute, direction, nones_order))
        return self

    def add_mass(self, *items: OrderOptionsTuple) -> "OrderOptionsBuilder":
        for item in items:
            self.add(*item)
        return self

    def build(self) -> OrderOptions:
        return OrderOptions(*self._params)


class OrderOptionsConverterInterface(abc.ABC):
    @abc.abstractmethod
    def convert(self, order: OrderOptions) -> OrderOptions:
        raise NotImplementedError()
