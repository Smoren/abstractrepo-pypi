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
    """Abstract Base Class defining the contract for synchronous CRUD repository operations.

    This interface specifies the standard Create, Read, Update, and Delete (CRUD) operations
    that any concrete synchronous repository implementation must adhere to. It promotes a
    clean separation of concerns, making application logic independent of the underlying
    data persistence mechanism.

    Type Parameters:
        TModel: The type of the model managed by the repository.
        TIdValueType: The type of the unique identifier (primary key) for the model.
        TCreateSchema: The type of the schema used for creating new models.
        TUpdateSchema: The type of the schema used for updating existing models.
    """
    @abc.abstractmethod
    def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[TModel, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[TModel]:
        """Retrieves a collection of items based on filtering, sorting, and pagination options.

        Args:
            filter_spec: An optional SpecificationInterface instance to filter the collection.
            order_options: An optional OrderOptions instance to specify the sorting order.
            paging_options: An optional PagingOptions instance to control pagination.

        Returns:
            A list of TModel instances matching the criteria.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def count(self, filter_spec: Optional[SpecificationInterface[TModel, bool]] = None) -> int:
        """Returns the total count of items matching the given filter specification.

         Args:
             filter_spec: An optional SpecificationInterface instance to filter the items.

         Returns:
             The number of items matching the filter.
         """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_item(self, item_id: TIdValueType) -> TModel:
        """Retrieves a single item by its unique identifier.

        Args:
            item_id: The unique identifier of the item to retrieve.

        Returns:
            The TModel instance corresponding to the item_id.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def exists(self, item_id: TIdValueType) -> bool:
        """Checks if an item with the specified ID exists in the repository.

        Args:
            item_id: The unique identifier of the item to check.

        Returns:
            True if an item with the specified ID exists, False otherwise.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, form: TCreateSchema) -> TModel:
        """Creates a new item in the repository using the provided creation form.

         Args:
             form: The TCreateSchema instance containing data for the new item.

         Returns:
             The newly created TModel instance.

        Raises:
            UniqueConstraintViolation: If a unique constraint violation occurs.
            RelationshipConstraintViolation: If a relationship constraint violation occurs.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModel:
        """Updates an existing item identified by its ID with data from the update form.

        Args:
            item_id: The unique identifier of the item to update.
            form: The TUpdateSchema instance containing data for updating the item.

        Returns:
            The updated TModel instance.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
            UniqueConstraintViolation: If a unique constraint violation occurs.
            RelationshipConstraintViolation: If a relationship constraint violation occurs.
       """
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, item_id: TIdValueType) -> TModel:
        """Deletes an item from the repository by its ID.

        Args:
            item_id: The unique identifier of the item to delete.

        Returns:
            The deleted TModel instance.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def model_class(self) -> Type[TModel]:
        """Returns the model class associated with the repository.

        This property should return the Python class that represents the data model
        (e.g., a Pydantic BaseModel, SQLAlchemy model, etc.) that this repository manages.

        Returns:
            The Type object representing the model class.
        """
        raise NotImplementedError()


class AsyncCrudRepositoryInterface(abc.ABC, Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema]):
    """Abstract Base Class defining the contract for asynchronous CRUD repository operations.

    This interface specifies the standard Create, Read, Update, and Delete (CRUD) operations
    that any concrete synchronous repository implementation must adhere to. It promotes a
    clean separation of concerns, making application logic independent of the underlying
    data persistence mechanism.

    Type Parameters:
        TModel: The type of the model managed by the repository.
        TIdValueType: The type of the unique identifier (primary key) for the model.
        TCreateSchema: The type of the schema used for creating new models.
        TUpdateSchema: The type of the schema used for updating existing models.
    """
    @abc.abstractmethod
    async def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[TModel, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[TModel]:
        """Retrieves a collection of items based on filtering, sorting, and pagination options.

        Args:
            filter_spec: An optional SpecificationInterface instance to filter the collection.
            order_options: An optional OrderOptions instance to specify the sorting order.
            paging_options: An optional PagingOptions instance to control pagination.

        Returns:
            A list of TModel instances matching the criteria.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def count(self, filter_spec: Optional[SpecificationInterface[TModel, bool]] = None) -> int:
        """Returns the total count of items matching the given filter specification.

        Args:
            filter_spec: An optional SpecificationInterface instance to filter the items.

        Returns:
            The number of items matching the filter.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_item(self, item_id: TIdValueType) -> TModel:
        """Retrieves a single item by its unique identifier.

        Args:
            item_id: The unique identifier of the item to retrieve.

        Returns:
            The TModel instance corresponding to the item_id.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def exists(self, item_id: TIdValueType) -> bool:
        """Checks if an item with the specified ID exists in the repository.

        Args:
            item_id: The unique identifier of the item to check.

        Returns:
            True if an item with the specified ID exists, False otherwise.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, form: TCreateSchema) -> TModel:
        """Creates a new item in the repository using the provided creation form.

        Args:
            form: The TCreateSchema instance containing data for the new item.

        Returns:
            The newly created TModel instance.

        Raises:
            UniqueConstraintViolation: If a unique constraint violation occurs.
            RelationshipConstraintViolation: If a relationship constraint violation occurs.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModel:
        """Updates an existing item identified by its ID with data from the update form.

        Args:
            item_id: The unique identifier of the item to update.
            form: The TUpdateSchema instance containing data for updating the item.

        Returns:
            The updated TModel instance.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
            UniqueConstraintViolation: If a unique constraint violation occurs.
            RelationshipConstraintViolation: If a relationship constraint violation occurs.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, item_id: TIdValueType) -> TModel:
        """Deletes an item from the repository by its ID.

        Args:
            item_id: The unique identifier of the item to delete.

        Returns:
            The deleted TModel instance.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def model_class(self) -> Type[TModel]:
        """Returns the model class associated with the repository.

        This property should return the Python class that represents the data model
        (e.g., a Pydantic BaseModel, SQLAlchemy model, etc.) that this repository manages.

        Returns:
            The Type object representing the model class.
        """
        raise NotImplementedError()


class ListBasedCrudRepository(
    Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    CrudRepositoryInterface[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    abc.ABC,
):
    """Implements a synchronous CRUD repository using an in-memory list.

    This class is a concrete implementation of the `CrudRepositoryInterface` using an in-memory list of items.
    """
    _db: List[TModel]

    def __init__(self, items: Optional[List[TModel]] = None):
        """Initializes the repository with an optional list of items.

        Args:
            items: The list of items to initialize the repository with.
        """
        self._db = items.copy() if items is not None else []

    def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[TModel, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[TModel]:
        """Retrieves a collection of items based on filtering, sorting, and pagination options.

        Args:
            filter_spec: An optional SpecificationInterface instance to filter the collection.
            order_options: An optional OrderOptions instance to specify the sorting order.
            paging_options: An optional PagingOptions instance to control pagination.

        Returns:
            A list of TModel instances matching the criteria.
        """
        result = self._db.copy()
        result = self._apply_filter(result, filter_spec)
        result = self._apply_order(result, order_options)
        result = self._apply_paging(result, paging_options)
        return result

    def count(self, filter_spec: Optional[SpecificationInterface[TModel, bool]] = None) -> int:
        """Returns the total count of items matching the given filter specification.

        Args:
            filter_spec: An optional SpecificationInterface instance to filter the items.

        Returns:
            The number of items matching the filter.
        """
        return len(self._apply_filter(self._db, filter_spec))

    def get_item(self, item_id: TIdValueType) -> TModel:
        """Retrieves a single item by its unique identifier.

        Args:
            item_id: The unique identifier of the item to retrieve.

        Returns:
            The TModel instance corresponding to the item_id.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        return self._find_by_id(item_id)

    def exists(self, item_id: TIdValueType) -> bool:
        """Checks if an item with the specified ID exists in the repository.

        Args:
            item_id: The unique identifier of the item to check.

        Returns:
            True if an item with the specified ID exists, False otherwise.
        """
        return bool(len(list(filter(lambda item: self._get_id_filter_specification(item_id).is_satisfied_by(item), self._db))))

    def create(self, form: TCreateSchema) -> TModel:
        """Creates a new item in the repository using the provided creation form.

        Args:
            form: The TCreateSchema instance containing data for the new item.

        Returns:
            The newly created TModel instance.

        Raises:
            UniqueConstraintViolation: If a unique constraint violation occurs.
            RelationshipConstraintViolation: If a relationship constraint violation occurs.
        """
        item = self._create_model(form, self._generate_id())
        self._db.append(item)
        return item

    def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModel:
        """Updates an existing item identified by its ID with data from the update form.

        Args:
            item_id: The unique identifier of the item to update.
            form: The TUpdateSchema instance containing data for updating the item.

        Returns:
            The updated TModel instance.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
            UniqueConstraintViolation: If a unique constraint violation occurs.
            RelationshipConstraintViolation: If a relationship constraint violation occurs.
        """
        return self._update_model(self._find_by_id(item_id), form)

    def delete(self, item_id: int) -> TModel:
        """Deletes an item from the repository by its ID.

        Args:
            item_id: The unique identifier of the item to delete.

        Returns:
            The deleted TModel instance.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        item = self._find_by_id(item_id)
        self._db = self._exclude_by_id(item_id)
        return item

    @abc.abstractmethod
    def _create_model(self, form: TCreateSchema, new_id: TIdValueType) -> TModel:
        """Creates a new item from the provided creation form and ID.

        Args:
            form: The TCreateSchema instance containing data for the new item.
            new_id: The new ID for the item.

        Returns:
            The newly created TModel instance.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _update_model(self, model: TModel, form: TUpdateSchema) -> TModel:
        """Updates an existing item with data from the update form.

        Args:
            model: The TModel instance to update.
            form: The TUpdateSchema instance containing data for updating the item.

        Returns:
            The updated TModel instance.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _generate_id(self) -> TIdValueType:
        """Generates a new unique identifier for a new item.
        raise NotImplementedError()

        Returns:
            The new unique identifier.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_id_filter_specification(self, item_id: TIdValueType) -> SpecificationInterface[TModel, bool]:
        """Returns a SpecificationInterface instance that filters items by their ID.

        Args:
            item_id: The ID of the item to filter by.

        Returns:
            The SpecificationInterface instance.
        """
        raise NotImplementedError()

    def _find_by_id(self, item_id: TIdValueType) -> TModel:
        """Finds an item by its ID.

        Args:
            item_id: The ID of the item to find.

        Returns:
            The TModel instance corresponding to the item_id.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        try:
            return next(filter(lambda item: self._get_id_filter_specification(item_id).is_satisfied_by(item), self._db))
        except StopIteration:
            raise ItemNotFoundException[TIdValueType](self.model_class, item_id)

    def _exclude_by_id(self, item_id: TIdValueType) -> List[TModel]:
        """Excludes an item from the repository by its ID.

        Args:
            item_id: The ID of the item to exclude.

        Returns:
            A list of items excluding the one with the ID.
        """
        return list(filter(lambda item: not self._get_id_filter_specification(item_id).is_satisfied_by(item), self._db))

    @staticmethod
    def _apply_filter(items: List[TModel], filter_spec: Optional[SpecificationInterface[TModel, bool]]) -> List[TModel]:
        """Applies a filter to the items using the provided filter specification.

        Args:
            items: The list of items to filter.
            filter_spec: The filter specification to apply.

        Returns:
            A list of items satisfying the filter specification.
        """
        if filter_spec is None:
            return items

        return list(filter(filter_spec.is_satisfied_by, items))

    @staticmethod
    def _apply_order(items: List[TModel], order_options: Optional[OrderOptions]) -> List[TModel]:
        """Applies ordering to the items using the provided order options.

        Args:
            items: The list of items to order.
            order_options: The order options to apply.

        Returns:
            A list of items sorted according to the order options.
        """
        if order_options is None:
            return items

        def get_none_key(order_option: OrderOption, value_is_none: bool) -> bool:
            """Returns the key to use for sorting null values.

            Args:
                order_option: The order option to use.
                value_is_none: Whether the value is null.

            Returns:
                The key to use for sorting.
            """
            if int(order_option.nones == NonesOrder.FIRST) ^ int(order_option.direction == OrderDirection.DESC):
                return not value_is_none
            else:
                return value_is_none

        def get_sort_key(order_option: OrderOption, item):
            """Returns the key to use for sorting the item.

            Args:
                order_option: The order option to use.
                item: The item to sort.

            Returns:
                The key to use for sorting.
            """
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
        """Applies paging to the items using the provided paging options.

        Args:
            items: The list of items to page.
            paging_options: The paging options to apply.

        Returns:
            A list of items satisfying the paging options.
        """
        if paging_options is None:
            return items

        return items[paging_options.offset:paging_options.offset + paging_options.limit]


class AsyncListBasedCrudRepository(
    Generic[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    AsyncCrudRepositoryInterface[TModel, TIdValueType, TCreateSchema, TUpdateSchema],
    abc.ABC,
):
    """Implements an asynchronous CRUD repository using an in-memory list.

    This class is a concrete implementation of the `AsyncCrudRepositoryInterface` using an in-memory list of items.
    """

    _db: List[TModel]

    def __init__(self, items: Optional[List[TModel]] = None):
        """Initializes the repository with an optional list of items.

        Args:
            items: The optional list of items to initialize the repository with.
        """
        self._db = items.copy() if items is not None else []

    async def get_collection(
        self,
        filter_spec: Optional[SpecificationInterface[TModel, bool]] = None,
        order_options: Optional[OrderOptions] = None,
        paging_options: Optional[PagingOptions] = None,
    ) -> List[TModel]:
        """Retrieves a collection of items based on filtering, sorting, and pagination options.

        Args:
            filter_spec: An optional SpecificationInterface instance to filter the items.
            order_options: An optional OrderOptions instance to specify the sorting order.
            paging_options: An optional PagingOptions instance to control pagination.

        Returns:
            A list of TModel instances matching the criteria.
        """
        result = self._db.copy()
        result = await self._apply_filter(result, filter_spec)
        result = await self._apply_order(result, order_options)
        result = await self._apply_paging(result, paging_options)
        return result

    async def count(self, filter_spec: Optional[SpecificationInterface[TModel, bool]] = None) -> int:
        """Returns the total count of items matching the given filter specification.

        Args:
            filter_spec: An optional SpecificationInterface instance to filter the items.

        Returns:
            The number of items matching the filter.
        """
        filtered = await self._apply_filter(self._db, filter_spec)
        return len(filtered)

    async def get_item(self, item_id: TIdValueType) -> TModel:
        """Retrieves a single item by its unique identifier.

        Args:
            item_id: The unique identifier of the item to retrieve.

        Returns:
            The TModel instance corresponding to the item_id.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        return await self._find_by_id(item_id)

    async def exists(self, item_id: TIdValueType) -> bool:
        """Returns whether an item with the given ID exists in the repository.

        Args:
            item_id: The unique identifier of the item to check.

        Returns:
            Whether the item exists.
        """
        filtered = await self._apply_filter(self._db, self._get_id_filter_specification(item_id))
        return bool(len(filtered))

    async def create(self, form: TCreateSchema) -> TModel:
        """Creates a new item in the repository using the provided creation form.

        Args:
            form: The creation form to create the item with.

        Returns:
            The created item.

        Raises:
            UniqueConstraintViolation: If a unique constraint violation occurs.
            RelationshipConstraintViolation: If a relationship constraint violation occurs.
        """
        item = await self._create_model(form, await self._generate_id())
        self._db.append(item)
        return item

    async def update(self, item_id: TIdValueType, form: TUpdateSchema) -> TModel:
        """Updates an existing item identified by its ID with data from the update form.

        Args:
            item_id: The unique identifier of the item to update.
            form: The update form to update the item with.

        Returns:
            The updated item.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
            UniqueConstraintViolation: If a unique constraint violation occurs.
            RelationshipConstraintViolation: If a relationship constraint violation occurs.
        """
        item = await self._find_by_id(item_id)
        return await self._update_model(item, form)

    async def delete(self, item_id: int) -> TModel:
        """Deletes an item from the repository by its ID.

        Args:
            item_id: The unique identifier of the item to delete.

        Returns:
            The deleted item.

        Raises:
            ItemNotFoundException[TIdValueType]: If no item with the specified ID is found.
        """
        item = await self._find_by_id(item_id)
        self._db = await self._exclude_by_id(item_id)
        return item

    @abc.abstractmethod
    async def _create_model(self, form: TCreateSchema, new_id: TIdValueType) -> TModel:
        """Creates a new item from the provided creation form and ID.

        Args:
            form: The creation form to create the item with.
            new_id: The ID to assign to the new item.

        Returns:
            The created item.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def _update_model(self, model: TModel, form: TUpdateSchema) -> TModel:
        """Updates an existing item with data from the update form.

        Args:
            model: The item to update.
            form: The update form to update the item with.

        Returns:
            The updated item.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def _generate_id(self) -> TIdValueType:
        """Generates a new unique ID for the next created item.

        Returns:
            The generated ID.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_id_filter_specification(self, item_id: TIdValueType) -> SpecificationInterface[TModel, bool]:
        """Returns a SpecificationInterface instance to filter items by the given ID.

        Args:
            item_id: The ID to filter by.

        Returns:
            A SpecificationInterface instance to filter items by the given ID.
        """
        raise NotImplementedError()

    async def _find_by_id(self, item_id: TIdValueType) -> TModel:
        """Finds an item by its ID and raises an ItemNotFoundException if not found.

        Args:
            item_id: The ID of the item to find.

        Returns:
            The found item.
        """
        filtered = await self._apply_filter(self._db, self._get_id_filter_specification(item_id))
        if not filtered:
            raise ItemNotFoundException[TIdValueType](self.model_class, item_id)
        return filtered[0]

    async def _exclude_by_id(self, item_id: TIdValueType) -> List[TModel]:
        """Excludes an item with the given ID from the repository.

        Args:
            item_id: The ID of the item to exclude.

        Returns:
            The modified repository.
        """
        return list(filter(lambda item: not self._get_id_filter_specification(item_id).is_satisfied_by(item), self._db))

    async def _apply_filter(
        self,
        items: List[TModel],
        filter_spec: Optional[SpecificationInterface[TModel, bool]]
    ) -> List[TModel]:
        """Applies a filter to the items using the provided filter specification.

        Args:
            items: The list of items to filter.
            filter_spec: An optional SpecificationInterface instance to filter the items.

        Returns:
            The filtered list of items.
        """
        if filter_spec is None:
            return items

        return list(filter(filter_spec.is_satisfied_by, items))

    @staticmethod
    async def _apply_order(items: List[TModel], order_options: Optional[OrderOptions]) -> List[TModel]:
        """Applies sorting to the items using the provided order options.

        Args:
            items: The list of items to sort.
            order_options: An optional OrderOptions instance to specify the sorting order.

        Returns:
            The sorted list of items.
        """
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
        """Applies pagination to the items using the provided paging options.

        Args:
            items: The list of items to page.
            paging_options: An optional PagingOptions instance to control pagination.

        Returns:
            The paged list of items.
        """
        if paging_options is None:
            return items

        return items[paging_options.offset:paging_options.offset + paging_options.limit]
