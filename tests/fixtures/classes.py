import abc
from typing import Optional, List

from abstractrepo.filter import SpecificationInterface, AttributeSpecification, Operator
from abstractrepo.order import OrderParams, OrderDirection
from abstractrepo.paging import PagingParams
from abstractrepo.repo import CrudRepositoryInterface, ListBasedCrudRepositoryInterface, TModel


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


class ListBasedNewsRepository(
    ListBasedCrudRepositoryInterface[News, int, NewsCreateForm, NewsUpdateForm],
    NewsRepositoryInterface,
):
    _next_id: int

    def __init__(self):
        super().__init__()
        self._next_id = 0

    def get_list(
        self,
        filter_spec: Optional[SpecificationInterface] = None,
        order_params: Optional[OrderParams] = None,
        paging_params: Optional[PagingParams] = None,
    ) -> List[News]:
        return list(super().get_list(filter_spec=filter_spec, order_params=order_params, paging_params=paging_params))

    @property
    def model_class(self) -> TModel:
        return News

    def _create_model(self, form: NewsCreateForm, new_id: int) -> News:
        return News(
            id=new_id,
            title=form.title,
            text=form.text
        )

    def _update_model(self, model: News, form: NewsUpdateForm) -> News:
        model.title = form.title
        model.text = form.text
        return model

    def _generate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _get_id_filter_specification(self, item_id: int) -> SpecificationInterface:
        return AttributeSpecification('id', item_id, Operator.E)

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
