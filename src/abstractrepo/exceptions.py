import functools
import warnings
from typing import Optional

try:
    from warnings import deprecated
except ImportError:  # pragma: no cover
    deprecated = lambda msg: lambda fn: functools.wraps(fn)(lambda *a, **kw: (warnings.warn(msg, category=DeprecationWarning, stacklevel=2), fn(*a, **kw))[1])  # pragma: no cover

from abstractrepo.specification import SpecificationInterface


class RepositoryExceptionInterface(Exception):
    pass


class ItemNotFoundException(RepositoryExceptionInterface):
    _model_class: type
    _item_id: Optional[int]
    _specification: Optional[SpecificationInterface]

    def __init__(self, model_class: type, item_id: Optional[int] = None, specification: Optional[SpecificationInterface] = None):
        msg = f'Item of type {model_class.__name__} not found'
        super().__init__(msg)
        self._model_class = model_class
        self._item_id = item_id
        self._specification = specification

    @property
    def model_class(self) -> type:
        return self._model_class

    @property
    @deprecated('Use model_class instead')
    def cls(self) -> type:
        return self._model_class

    @property
    def item_id(self) -> Optional[int]:
        return self._item_id

    @property
    def specification(self) -> Optional[SpecificationInterface]:
        return self._specification


class UniqueViolationException(RepositoryExceptionInterface):
    _model_class: type
    _action: str
    _form: object

    def __init__(self, model_class: type, action: str, form: object):
        super().__init__(f'Action {action} of {model_class.__name__} instance failed due to unique violation')
        self._model_class = model_class
        self._action = action
        self._form = form

    @property
    def model_class(self) -> type:
        return self._model_class

    @property
    @deprecated('Use model_class instead')
    def cls(self) -> type:
        return self._model_class

    @property
    def action(self) -> str:
        return self._action

    @property
    def form(self) -> object:
        return self._form


class RelationViolationException(RepositoryExceptionInterface):
    _model_class: type
    _action: str
    _form: object

    def __init__(self, model_class: type, action: str, form: object):
        super().__init__(f'Action {action} of {model_class.__name__} instance failed due to relation violation')
        self._model_class = model_class
        self._action = action
        self._form = form

    @property
    def model_class(self) -> type:
        return self._model_class

    @property
    @deprecated('Use model_class instead')
    def cls(self) -> type:
        return self._model_class

    @property
    def action(self) -> str:
        return self._action

    @property
    def form(self) -> object:
        return self._form
