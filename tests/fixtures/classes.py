import abc
from typing import Optional, List

from abstractrepo.exceptions import ItemNotFoundException

from abstractrepo.filter import SpecificationInterface
from abstractrepo.order import OrderParams, OrderDirection
from abstractrepo.paging import PagingParams
from abstractrepo.repo import CrudRepositoryInterface


class News:
    id: int
    title: str
    text: str

    def __init__(self, id: int, title: str, text: str):
        self.id = id
        self.title = title
        self.text = text


class NewsCreateForm:
    title: str
    text: str

    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text


class NewsUpdateForm:
    title: str
    text: str

    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text


class NewsRepositoryInterface(CrudRepositoryInterface[News, int, NewsCreateForm, NewsUpdateForm], abc.ABC):
    pass


class ExampleNewsRepository(NewsRepositoryInterface):
    _db: List[News]
    _next_id: int

    def __init__(self):
        self._db = []
        self._next_id = 1

    def get_list(
        self,
        filter_spec: Optional[SpecificationInterface] = None,
        order_params: Optional[OrderParams] = None,
        paging_params: Optional[PagingParams] = None,
    ) -> List[News]:
        result = self._db.copy()
        result = self._apply_filter(result, filter_spec)
        result = self._apply_order(result, order_params)
        result = self._apply_paging(result, paging_params)
        return result

    def get_item(self, item_id: int) -> News:
        try:
            return next(filter(lambda news: news.id == item_id, self._db))
        except StopIteration:
            raise ItemNotFoundException(News, item_id)

    def create(self, form: NewsCreateForm) -> News:
        new_news = News(
            id=self._next_id,
            title=form.title,
            text=form.text
        )
        self._db.append(new_news)
        self._next_id += 1
        return new_news

    def update(self, item_id: int, form: NewsUpdateForm) -> News:
        try:
            news = next(filter(lambda news: news.id == item_id, self._db))
            news.title = form.title
            news.text = form.text
            return news
        except StopIteration:
            raise ItemNotFoundException(News, item_id)

    def delete(self, item_id: int) -> News:
        filtered_db = list(filter(lambda news: news.id != item_id, self._db))
        if len(filtered_db) == len(self._db):
            raise ItemNotFoundException(News, item_id)
        self._db = filtered_db

    @staticmethod
    def _apply_filter(items: List[News], filter_spec: Optional[SpecificationInterface]) -> List[News]:
        if filter_spec is None:
            return items

        return list(filter(filter_spec.is_satisfied_by, items))

    @staticmethod
    def _apply_order(items: List[News], order_params: Optional[OrderParams]) -> List[News]:
        if order_params is None:
            return items

        for order_param in reversed(order_params.params):
            items = sorted(
                items,
                key=lambda news: getattr(news, order_param.attribute),
                reverse=order_param.direction == OrderDirection.DESC,
            )

        return items

    @staticmethod
    def _apply_paging(items: List[News], paging_params: Optional[PagingParams]) -> List[News]:
        if paging_params is None:
            return items

        return items[paging_params.offset:paging_params.offset+paging_params.limit]
