from typing import Optional


class PagingOptions:
    limit: Optional[int]
    offset: Optional[int]

    def __init__(self, limit: Optional[int] = None, offset: Optional[int] = None):
        self.limit = limit
        self.offset = offset


class Paginator:
    _page_size: int

    def __init__(self, page_size: int):
        self._page_size = page_size

    def get_paging_options(self, page_number: int) -> PagingOptions:
        return PagingOptions(limit=self._page_size, offset=(page_number - 1) * self._page_size)
