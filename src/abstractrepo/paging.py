import abc
from typing import Optional


class PagingOptions:
    """Represents options for pagination, including limit and offset.

    Attributes:
        limit: The maximum number of items to return. If None, no limit is applied.
        offset: The number of items to skip from the beginning. If None, no offset is applied.
    """
    limit: Optional[int]
    offset: Optional[int]

    def __init__(self, limit: Optional[int] = None, offset: Optional[int] = None):
        self.limit = limit
        self.offset = offset


class PageResolver:
    """A utility class for resolving page numbers into PagingOptions.

    This class helps in converting a human-readable page number into the
    corresponding limit and offset values required for pagination.
    """
    _page_size: int
    _start_page: int

    def __init__(self, page_size: int, start_page: int = 0):
        """Initializes a new PageResolver.

        Args:
            page_size: The number of items to include in each page.
            start_page: The starting page number. Defaults to 0 (0-indexed pages).
        """
        self._page_size = page_size
        self._start_page = start_page

    def get_page(self, page_number: int) -> PagingOptions:
        """Calculates the PagingOptions for a given page number.

        Args:
            page_number: The desired page number.

        Returns:
            A PagingOptions instance with the calculated limit and offset.
        """
        return PagingOptions(limit=self._page_size, offset=(page_number - self._start_page) * self._page_size)


class PagingOptionsConverterInterface(abc.ABC):
    """Abstract base class for converting PagingOptions.

    This interface defines a method for converting a PagingOptions instance,
    which can be useful for adapting pagination criteria to different contexts
    or underlying data stores.
    """
    @abc.abstractmethod
    def convert(self, order: PagingOptions) -> PagingOptions:
        """Converts a PagingOptions instance.

        Args:
            order: The PagingOptions instance to convert.

        Returns:
            A new PagingOptions instance after conversion.
        """
        raise NotImplementedError()
