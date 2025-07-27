import abc
from typing import Optional


class PagingOptions:
    limit: Optional[int]
    offset: Optional[int]

    def __init__(self, limit: Optional[int] = None, offset: Optional[int] = None):
        self.limit = limit
        self.offset = offset


class PageResolver:
    _page_size: int
    _start_page: int

    def __init__(self, page_size: int, start_page: int = 0):
        self._page_size = page_size
        self._start_page = start_page

    def get_page(self, page_number: int) -> PagingOptions:
        return PagingOptions(limit=self._page_size, offset=(page_number - self._start_page) * self._page_size)


class PagingOptionsConverterInterface(abc.ABC):
    @abc.abstractmethod
    def convert(self, order: PagingOptions) -> PagingOptions:
        raise NotImplementedError()
