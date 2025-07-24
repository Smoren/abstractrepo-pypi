import abc
from typing import Optional, List

from abstractrepo.exceptions import ItemNotFoundException

from abstractrepo.filter import SpecificationInterface
from abstractrepo.order import OrderParams
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
    _db: List[News] = []
    _next_id: int = 1

    def get_list(
        self,
        filter_spec: Optional[SpecificationInterface] = None,
        order_params: Optional[OrderParams] = None,
        paging_params: Optional[PagingParams] = None,
    ) -> List[News]:
        return self._db.copy()

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
