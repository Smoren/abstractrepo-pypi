from typing import List, TypeVar, Generic, Optional
import abc

from abstractrepo.order import OrderParams
from abstractrepo.paging import PagingParams
from abstractrepo.filter import SpecificationInterface

TModelSchema = TypeVar('TModelSchema')
TIdValueType = TypeVar('TIdValueType')
TCreateSchema = TypeVar('TCreateSchema')
TUpdateSchema = TypeVar('TUpdateSchema')
TDbModel = TypeVar('TDbModel')


class CrudRepositoryInterface(abc.ABC, Generic[TModelSchema, TIdValueType, TCreateSchema, TUpdateSchema]):
    @abc.abstractmethod
    def get_list(
        self,
        filter_spec: Optional[SpecificationInterface] = None,
        order_params: Optional[OrderParams] = None,
        paging_params: Optional[PagingParams] = None,
    ) -> List[TModelSchema]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_item(self, item_id: TIdValueType) -> TModelSchema:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, form: TCreateSchema) -> TModelSchema:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModelSchema:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, item_id: TIdValueType) -> TModelSchema:
        raise NotImplementedError()
