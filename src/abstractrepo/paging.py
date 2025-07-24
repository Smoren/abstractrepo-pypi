from typing import Optional


class PagingParams:
    limit: Optional[int]
    offset: Optional[int]

    def __init__(self, limit: Optional[int], offset: Optional[int]):
        self.limit = limit
        self.offset = offset
