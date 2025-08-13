import functools
import warnings
from typing import Optional, Generic, TypeVar

try:
    from warnings import deprecated
except ImportError:  # pragma: no cover
    deprecated = lambda msg: lambda fn: functools.wraps(fn)(lambda *a, **kw: (warnings.warn(msg, category=DeprecationWarning, stacklevel=2), fn(*a, **kw))[1])  # pragma: no cover

from abstractrepo.specification import SpecificationInterface

TIdValueType = TypeVar('TIdValueType')


class RepositoryExceptionInterface(Exception):
    """Base interface for all repository-related exceptions.

    All custom exceptions raised by repository operations should inherit from this class.
    """
    pass


class ItemNotFoundException(Generic[TIdValueType], RepositoryExceptionInterface):
    """Exception raised when a requested item is not found in the repository."""
    _model_class: type
    _item_id: Optional[TIdValueType]
    _specification: Optional[SpecificationInterface]

    def __init__(self, model_class: type, item_id: Optional[TIdValueType] = None, specification: Optional[SpecificationInterface] = None):
        """Initializes a new ItemNotFoundException.

        Args:
            model_class: The class of the model that was expected but not found.
            item_id: Optional. The specific ID of the item that was not found.
            specification: Optional. The specification used in the search that yielded no results.
        """
        msg = f'Item of type {model_class.__name__} not found'
        super().__init__(msg)
        self._model_class = model_class
        self._item_id = item_id
        self._specification = specification

    @property
    def model_class(self) -> type:
        """Returns the model class associated with the exception."""
        return self._model_class

    @property
    @deprecated('Use model_class instead')
    def cls(self) -> type:
        """Deprecated: Use model_class instead."""
        return self._model_class

    @property
    def item_id(self) -> Optional[TIdValueType]:
        """Returns the ID of the item that was not found."""
        return self._item_id

    @property
    def specification(self) -> Optional[SpecificationInterface]:
        """Returns the specification used when the item was not found."""
        return self._specification


class UniqueViolationException(RepositoryExceptionInterface):
    """Exception raised when a unique constraint is violated during a repository operation.

    This typically occurs during create or update operations when an attempt is made
    to insert or modify data that would result in a duplicate value in a unique field.
    """
    _model_class: type
    _action: str
    _form: object

    def __init__(self, model_class: type, action: str, form: object):
        """Initializes a new UniqueViolationException.

        Args:
            model_class: The class of the model on which the unique constraint was violated.
            action: A string describing the action that led to the violation (e.g., "create", "update").
            form: The form object that was being processed when the violation occurred.
        """
        super().__init__(f'Action {action} of {model_class.__name__} instance failed due to unique violation')
        self._model_class = model_class
        self._action = action
        self._form = form

    @property
    def model_class(self) -> type:
        """Returns the model class associated with the exception."""
        return self._model_class

    @property
    @deprecated('Use model_class instead')
    def cls(self) -> type:
        """Deprecated: Use model_class instead."""
        return self._model_class

    @property
    def action(self) -> str:
        """Returns the action that caused the unique violation."""
        return self._action

    @property
    def form(self) -> object:
        """Returns the form data that led to the unique violation."""
        return self._form


class RelationViolationException(RepositoryExceptionInterface):
    """Exception raised when a foreign key or other relation constraint is violated.

    This can occur, for example, when attempting to delete a parent record that still
    has associated child records, or when creating a record with a non-existent foreign key.
    """
    _model_class: type
    _action: str
    _form: object

    def __init__(self, model_class: type, action: str, form: object):
        """Initializes a new RelationViolationException.

        Args:
            model_class: The class of the model on which the relation constraint was violated.
            action: A string describing the action that led to the violation (e.g., "create", "update", "delete").
            form: The form object or model instance that was being processed when the violation occurred.
        """
        super().__init__(f'Action {action} of {model_class.__name__} instance failed due to relation violation')
        self._model_class = model_class
        self._action = action
        self._form = form

    @property
    def model_class(self) -> type:
        """Returns the model class associated with the exception."""
        return self._model_class

    @property
    @deprecated('Use model_class instead')
    def cls(self) -> type:
        """Deprecated: Use model_class instead."""
        return self._model_class

    @property
    def action(self) -> str:
        """Returns the action that caused the relation violation."""
        return self._action

    @property
    def form(self) -> object:
        """Returns the form data that led to the relation violation."""
        return self._form
