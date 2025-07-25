from typing import List, TypeVar, Generic, Optional, Callable, Iterable
import abc

from abstractrepo.exceptions import ItemNotFoundException

from abstractrepo.order import OrderParams, OrderDirection
from abstractrepo.paging import PagingParams
from abstractrepo.filter import SpecificationInterface

TModel = TypeVar('TModel')
TIdValueType = TypeVar('TIdValueType')
TCreateSchema = TypeVar('TCreateSchema')
TUpdateSchema = TypeVar('TUpdateSchema')


class CrudRepositoryInterface(abc.ABC, Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema]):
    @abc.abstractmethod
    def get_list(
        self,
        filter_spec: Optional[SpecificationInterface] = None,
        order_params: Optional[OrderParams] = None,
        paging_params: Optional[PagingParams] = None,
    ) -> Iterable[TModel]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_item(self, item_id: TIdValueType) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    def exists(self, item_id: TIdValueType) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, form: TCreateSchema) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, item_id: TIdValueType) -> TModel:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def model_class(self) -> TModel:
        raise NotImplementedError()


class ListBasedCrudRepositoryInterface(
    Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    CrudRepositoryInterface[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    abc.ABC,
):
    _db: List[TModel]

    def __init__(self):
        self._db = []

    def get_list(
        self,
        filter_spec: Optional[SpecificationInterface] = None,
        order_params: Optional[OrderParams] = None,
        paging_params: Optional[PagingParams] = None,
    ) -> Iterable[TModel]:
        result = self._db.copy()
        result = self._apply_filter(result, filter_spec)
        result = self._apply_order(result, order_params)
        result = self._apply_paging(result, paging_params)
        return result

    def get_item(self, item_id: TIdValueType) -> TModel:
        return self._find_by_id(item_id)

    def exists(self, item_id: TIdValueType) -> bool:
        return bool(len(list(filter(self._get_id_filter_condition(item_id), self._db))))

    def create(self, form: TCreateSchema) -> TModel:
        item = self._create_model(form, self._generate_id())
        self._db.append(item)
        return item

    def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModel:
        return self._update_model(self._find_by_id(item_id), form)

    def delete(self, item_id: int) -> TModel:
        item = self._find_by_id(item_id)
        self._db = self._exclude_by_id(item_id)
        return item

    @abc.abstractmethod
    def _create_model(self, form: TCreateSchema, new_id: TIdValueType) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    def _update_model(self, model: TModel, form: TUpdateSchema) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    def _generate_id(self) -> TIdValueType:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_id_filter_condition(self, item_id: TIdValueType) -> Callable[[TModel], bool]:
        raise NotImplementedError()

    def _find_by_id(self, item_id: TIdValueType) -> TModel:
        try:
            return next(filter(self._get_id_filter_condition(item_id), self._db))
        except StopIteration:
            raise ItemNotFoundException(self.model_class, item_id)

    def _exclude_by_id(self, item_id: TIdValueType) -> TModel:
        return list(filter(lambda item: not self._get_id_filter_condition(item_id)(item), self._db))

    @staticmethod
    def _apply_filter(items: List[TModel], filter_spec: Optional[SpecificationInterface]) -> List[TModel]:
        if filter_spec is None:
            return items

        return list(filter(filter_spec.is_satisfied_by, items))

    @staticmethod
    def _apply_order(items: List[TModel], order_params: Optional[OrderParams]) -> List[TModel]:
        if order_params is None:
            return items

        for order_param in reversed(order_params.params):
            items = sorted(
                items,
                key=lambda item: getattr(item, order_param.attribute),
                reverse=order_param.direction == OrderDirection.DESC,
            )

        return items

    @staticmethod
    def _apply_paging(items: List[TModel], paging_params: Optional[PagingParams]) -> List[TModel]:
        if paging_params is None:
            return items

        return items[paging_params.offset:paging_params.offset+paging_params.limit]
