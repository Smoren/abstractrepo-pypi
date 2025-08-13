from typing import List, TypeVar, Generic, Optional, Type
import abc

from abstractrepo.exceptions import ItemNotFoundException

from abstractrepo.order import OrderOptions, OrderDirection, NonesOrder, OrderOption
from abstractrepo.paging import PagingOptions
from abstractrepo.specification import SpecificationInterface

TModel = TypeVar('TModel')
TIdValueType = TypeVar('TIdValueType')
TCreateSchema = TypeVar('TCreateSchema')
TUpdateSchema = TypeVar('TUpdateSchema')


class CrudRepositoryInterface(abc.ABC, Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema]):
    @abc.abstractmethod
    def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[TModel, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[TModel]:
        raise NotImplementedError()

    @abc.abstractmethod
    def count(self, filter_spec: Optional[SpecificationInterface[TModel, bool]] = None) -> int:
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
    def model_class(self) -> Type[TModel]:
        raise NotImplementedError()


class AsyncCrudRepositoryInterface(abc.ABC, Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema]):
    @abc.abstractmethod
    async def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[TModel, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[TModel]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count(self, filter_spec: Optional[SpecificationInterface[TModel, bool]] = None) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_item(self, item_id: TIdValueType) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    async def exists(self, item_id: TIdValueType) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, form: TCreateSchema) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, item_id: TIdValueType) -> TModel:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def model_class(self) -> Type[TModel]:
        raise NotImplementedError()


class ListBasedCrudRepository(
    Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    CrudRepositoryInterface[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    abc.ABC,
):
    _db: List[TModel]

    def __init__(self, items: Optional[List[TModel]] = None):
        self._db = items.copy() if items is not None else []

    def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[TModel, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[TModel]:
        result = self._db.copy()
        result = self._apply_filter(result, filter_spec)
        result = self._apply_order(result, order_options)
        result = self._apply_paging(result, paging_options)
        return result

    def count(self, filter_spec: Optional[SpecificationInterface[TModel, bool]] = None) -> int:
        return len(self._apply_filter(self._db, filter_spec))

    def get_item(self, item_id: TIdValueType) -> TModel:
        return self._find_by_id(item_id)

    def exists(self, item_id: TIdValueType) -> bool:
        return bool(len(list(filter(lambda item: self._get_id_filter_specification(item_id).is_satisfied_by(item), self._db))))

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
    def _get_id_filter_specification(self, item_id: TIdValueType) -> SpecificationInterface[TModel, bool]:
        raise NotImplementedError()

    def _find_by_id(self, item_id: TIdValueType) -> TModel:
        try:
            return next(filter(lambda item: self._get_id_filter_specification(item_id).is_satisfied_by(item), self._db))
        except StopIteration:
            raise ItemNotFoundException(self.model_class, item_id)

    def _exclude_by_id(self, item_id: TIdValueType) -> TModel:
        return list(filter(lambda item: not self._get_id_filter_specification(item_id).is_satisfied_by(item), self._db))

    @staticmethod
    def _apply_filter(items: List[TModel], filter_spec: Optional[SpecificationInterface[TModel, bool]]) -> List[TModel]:
        if filter_spec is None:
            return items

        return list(filter(filter_spec.is_satisfied_by, items))

    @staticmethod
    def _apply_order(items: List[TModel], order_options: Optional[OrderOptions]) -> List[TModel]:
        if order_options is None:
            return items

        def get_none_key(order_option: OrderOption, value_is_none: bool) -> bool:
            if int(order_option.nones == NonesOrder.FIRST) ^ int(order_option.direction == OrderDirection.DESC):
                return not value_is_none
            else:
                return value_is_none

        def get_sort_key(order_option: OrderOption, item):
            value = getattr(item, option.attribute)
            none_key = get_none_key(order_option, value is None)
            return none_key, value

        for option in reversed(order_options.options):
            items = sorted(
                items,
                key=lambda item: get_sort_key(option, item),
                reverse=option.direction == OrderDirection.DESC,
            )

        return items

    @staticmethod
    def _apply_paging(items: List[TModel], paging_options: Optional[PagingOptions]) -> List[TModel]:
        if paging_options is None:
            return items

        return items[paging_options.offset:paging_options.offset + paging_options.limit]


class AsyncListBasedCrudRepository(
    Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    AsyncCrudRepositoryInterface[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    abc.ABC,
):
    _db: List[TModel]

    def __init__(self, items: Optional[List[TModel]] = None):
        self._db = items.copy() if items is not None else []

    async def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[TModel, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[TModel]:
        result = self._db.copy()
        result = await self._apply_filter(result, filter_spec)
        result = await self._apply_order(result, order_options)
        result = await self._apply_paging(result, paging_options)
        return result

    async def count(self, filter_spec: Optional[SpecificationInterface[TModel, bool]] = None) -> int:
        filtered = await self._apply_filter(self._db, filter_spec)
        return len(filtered)

    async def get_item(self, item_id: TIdValueType) -> TModel:
        return await self._find_by_id(item_id)

    async def exists(self, item_id: TIdValueType) -> bool:
        filtered = await self._apply_filter(self._db, self._get_id_filter_specification(item_id))
        return bool(len(filtered))

    async def create(self, form: TCreateSchema) -> TModel:
        item = await self._create_model(form, await self._generate_id())
        self._db.append(item)
        return item

    async def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModel:
        item = await self._find_by_id(item_id)
        return await self._update_model(item, form)

    async def delete(self, item_id: int) -> TModel:
        item = await self._find_by_id(item_id)
        self._db = await self._exclude_by_id(item_id)
        return item

    @abc.abstractmethod
    async def _create_model(self, form: TCreateSchema, new_id: TIdValueType) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    async def _update_model(self, model: TModel, form: TUpdateSchema) -> TModel:
        raise NotImplementedError()

    @abc.abstractmethod
    async def _generate_id(self) -> TIdValueType:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_id_filter_specification(self, item_id: TIdValueType) -> SpecificationInterface[TModel, bool]:
        raise NotImplementedError()

    async def _find_by_id(self, item_id: TIdValueType) -> TModel:
        filtered = await self._apply_filter(self._db, self._get_id_filter_specification(item_id))
        if not filtered:
            raise ItemNotFoundException(self.model_class, item_id)
        return filtered[0]

    async def _exclude_by_id(self, item_id: TIdValueType) -> List[TModel]:
        return list(filter(lambda item: not self._get_id_filter_specification(item_id).is_satisfied_by(item), self._db))

    async def _apply_filter(
        self,
        items: List[TModel],
        filter_spec: Optional[SpecificationInterface[TModel, bool]]
    ) -> List[TModel]:
        if filter_spec is None:
            return items

        return list(filter(filter_spec.is_satisfied_by, items))

    @staticmethod
    async def _apply_order(items: List[TModel], order_options: Optional[OrderOptions]) -> List[TModel]:
        if order_options is None:
            return items

        def get_none_key(order_option: OrderOption, value_is_none: bool) -> bool:
            if int(order_option.nones == NonesOrder.FIRST) ^ int(order_option.direction == OrderDirection.DESC):
                return not value_is_none
            else:
                return value_is_none

        def get_sort_key(order_option: OrderOption, item):
            value = getattr(item, option.attribute)
            none_key = get_none_key(order_option, value is None)
            return none_key, value

        for option in reversed(order_options.options):
            items = sorted(
                items,
                key=lambda item: get_sort_key(option, item),
                reverse=option.direction == OrderDirection.DESC,
            )

        return items

    @staticmethod
    async def _apply_paging(items: List[TModel], paging_options: Optional[PagingOptions]) -> List[TModel]:
        if paging_options is None:
            return items

        return items[paging_options.offset:paging_options.offset + paging_options.limit]
