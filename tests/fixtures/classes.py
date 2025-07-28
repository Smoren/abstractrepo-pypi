import abc
from typing import Optional, List, Union, Type

from abstractrepo.specification import SpecificationInterface, Operator, AttributeSpecification
from abstractrepo.order import OrderOptions
from abstractrepo.paging import PagingOptions
from abstractrepo.repo import CrudRepositoryInterface, ListBasedCrudRepository


class News:
    id: int
    title: str
    text: Optional[str]

    def __init__(self, id: int, title: str, text: Optional[str] = None):
        self.id = id
        self.title = title
        self.text = text


class NewsCreateForm:
    title: str
    text: Union[str, None]

    def __init__(self, title: str, text: Optional[str] = None):
        self.title = title
        self.text = text


class NewsUpdateForm:
    title: str
    text: str

    def __init__(self, title: str, text: Optional[str] = None):
        self.title = title
        self.text = text


class NewsRepositoryInterface(CrudRepositoryInterface[News, int, NewsCreateForm, NewsUpdateForm], abc.ABC):
    pass


class ListBasedNewsRepository(
    ListBasedCrudRepository[News, int, NewsCreateForm, NewsUpdateForm],
    NewsRepositoryInterface,
):
    _next_id: int

    def __init__(self, items: Optional[List[News]] = None):
        super().__init__(items)
        self._next_id = 0

    def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[News, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[News]:
        return list(super().get_collection(filter_spec=filter_spec, order_options=order_options, paging_options=paging_options))

    @property
    def model_class(self) -> Type[News]:
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

    def _get_id_filter_specification(self, item_id: int) -> SpecificationInterface[News, bool]:
        return AttributeSpecification('id', item_id, Operator.E)
