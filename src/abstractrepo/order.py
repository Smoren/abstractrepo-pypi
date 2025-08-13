import abc
from enum import Enum
from typing import List, Tuple, Union, Optional


class OrderDirection(Enum):
    """Enumeration for specifying the direction of ordering.

    Attributes:
        ASC: Ascending order.
        DESC: Descending order.
    """
    ASC = 'ASC'
    DESC = 'DESC'


class NonesOrder(Enum):
    """Enumeration for specifying the placement of NULL/None values in ordered results.

    Attributes:
        FIRST: NULL/None values appear first.
        LAST: NULL/None values appear last.
    """
    FIRST = 'FIRST'
    LAST = 'LAST'


OrderOptionsTuple = Union[Tuple[str], Tuple[str, OrderDirection], Tuple[str, OrderDirection, NonesOrder]]


class OrderOption:
    """Represents a single ordering criterion for a collection.

    Defines an attribute to sort by, the direction of sorting (ascending/descending),
    and how None values should be handled.

    Attributes:
        attribute: The name of the attribute to sort by.
        direction: The direction of sorting (ASC or DESC).
        nones: The placement of None values (FIRST or LAST).
    """
    attribute: str
    direction: OrderDirection
    nones: NonesOrder

    def __init__(self, attribute: str, direction: OrderDirection, nones: Optional[NonesOrder] = None):
        """Initializes a new OrderOption.

        Args:
            attribute: The name of the attribute to sort by.
            direction: The direction of sorting (OrderDirection.ASC or OrderDirection.DESC).
            nones: Optional. Specifies where None values should be placed. If not provided,
                   defaults to LAST for ASC and FIRST for DESC.
        """
        self.attribute = attribute
        self.direction = direction
        self._set_nones(nones)

    def _set_nones(self, nones: NonesOrder) -> None:
        """Sets the nones order, applying defaults if not explicitly provided."""
        if nones is not None:
            self.nones = nones
            return

        if self.direction == OrderDirection.ASC:
            self.nones = NonesOrder.LAST
        else:
            self.nones = NonesOrder.FIRST


class OrderOptions:
    """A collection of OrderOption instances, defining multiple sorting criteria.

    Sorting is applied in the order the options are added.
    """
    _options: List[OrderOption]

    def __init__(self, *options: OrderOption):
        """Initializes a new OrderOptions instance.

         Args:
             *options: One or more OrderOption instances.
         """
        self._options = list(options)

    @property
    def options(self):
        """Returns the list of order options.

        Returns:
            A list of OrderOption instances.
        """
        return self._options


class OrderOptionsBuilder:
    """A builder class for constructing OrderOptions instances.

    Provides a fluent interface for adding multiple ordering criteria.
    """
    _options: List[OrderOption]

    def __init__(self):
        """Initializes a new OrderOptionsBuilder."""
        self._options = []

    def add(self, attribute: str, direction: OrderDirection = OrderDirection.ASC, nones: Optional[NonesOrder] = None) -> "OrderOptionsBuilder":
        """Adds a single order option to the builder.

        Args:
            attribute: The name of the attribute to sort by.
            direction: The direction of sorting. Defaults to OrderDirection.ASC.
            nones: Optional. Specifies where None values should be placed.

        Returns:
            The OrderOptionsBuilder instance for chaining.
        """
        self._options.append(OrderOption(attribute, direction, nones))
        return self

    def add_mass(self, *items: OrderOptionsTuple) -> "OrderOptionsBuilder":
        """Adds multiple order options from tuples.

        Each tuple can be:
        - (attribute_name,)
        - (attribute_name, OrderDirection)
        - (attribute_name, OrderDirection, NonesOrder)

        Args:
            *items: Variable number of tuples, each representing an order option.

        Returns:
            The OrderOptionsBuilder instance for chaining.
        """
        for item in items:
            self.add(*item)
        return self

    def build(self) -> OrderOptions:
        """Builds and returns the OrderOptions instance.

        Returns:
            An OrderOptions instance containing all added order criteria.
        """
        return OrderOptions(*self._options)


class OrderOptionsConverterInterface(abc.ABC):
    """Abstract base class for converting OrderOptions.

    This interface defines a method for converting an OrderOptions instance,
    which can be useful for adapting ordering criteria to different contexts
    or underlying data stores.
    """
    @abc.abstractmethod
    def convert(self, order: OrderOptions) -> OrderOptions:
        """Converts an OrderOptions instance.

        Args:
            order: The OrderOptions instance to convert.

        Returns:
            A new OrderOptions instance after conversion.
        """
        raise NotImplementedError()
