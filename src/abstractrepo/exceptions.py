from typing import Optional

from abstractrepo.specification import SpecificationInterface


class RepositoryExceptionInterface(Exception):
    pass


class ItemNotFoundException(RepositoryExceptionInterface):
    _cls: type
    _item_id: Optional[int]
    _specification: Optional[SpecificationInterface]

    def __init__(self, cls: type, item_id: Optional[int] = None, specification: Optional[SpecificationInterface] = None):
        msg = f'Item of type {cls.__name__} not found'
        super().__init__(msg)
        self._cls = cls
        self._item_id = item_id
        self._specification = specification

    @property
    def cls(self) -> type:
        return self._cls

    @property
    def item_id(self) -> Optional[int]:
        return self._item_id

    @property
    def specification(self) -> Optional[SpecificationInterface]:
        return self._specification


class UniqueViolationException(RepositoryExceptionInterface):
    _cls: type
    _action: str
    _form: object

    def __init__(self, cls: type, action: str, form: object):
        super().__init__(f'Action {action} of {cls.__name__} instance failed due to unique violation')
        self._cls = cls
        self._action = action
        self._form = form

    @property
    def cls(self) -> type:
        return self._cls

    @property
    def action(self) -> str:
        return self._action

    @property
    def form(self) -> object:
        return self._form


class RelationViolationException(RepositoryExceptionInterface):
    _cls: type
    _action: str
    _form: object

    def __init__(self, cls: type, action: str, form: object):
        super().__init__(f'Action {action} of {cls.__name__} instance failed due to relation violation')
        self._cls = cls
        self._action = action
        self._form = form

    @property
    def cls(self) -> type:
        return self._cls

    @property
    def action(self) -> str:
        return self._action

    @property
    def form(self) -> object:
        return self._form
