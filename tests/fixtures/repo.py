import abc
from typing import Optional, List, Type

from abstractrepo.exceptions import ItemNotFoundException, UniqueViolationException
from abstractrepo.specification import SpecificationInterface, Operator, AttributeSpecification
from abstractrepo.repo import CrudRepositoryInterface, ListBasedCrudRepository, AsyncCrudRepositoryInterface, \
    AsyncListBasedCrudRepository
from tests.fixtures.models import News, NewsCreateForm, NewsUpdateForm, User, UserCreateForm, UserUpdateForm


class NewsRepositoryInterface(CrudRepositoryInterface[News, int, NewsCreateForm, NewsUpdateForm], abc.ABC):
    pass


class AsyncNewsRepositoryInterface(AsyncCrudRepositoryInterface[News, int, NewsCreateForm, NewsUpdateForm], abc.ABC):
    pass


class UserRepositoryInterface(CrudRepositoryInterface[User, int, UserCreateForm, UserUpdateForm], abc.ABC):
    pass


class AsyncUserRepositoryInterface(AsyncCrudRepositoryInterface[User, int, UserCreateForm, UserUpdateForm], abc.ABC):
    pass


class ListBasedNewsRepository(
    ListBasedCrudRepository[News, int, NewsCreateForm, NewsUpdateForm],
    NewsRepositoryInterface,
):
    _next_id: int

    def __init__(self, items: Optional[List[News]] = None):
        super().__init__(items)
        self._next_id = 0

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


class AsyncListBasedNewsRepository(
    AsyncListBasedCrudRepository[News, int, NewsCreateForm, NewsUpdateForm],
    AsyncNewsRepositoryInterface,
):
    _next_id: int

    def __init__(self, items: Optional[List[News]] = None):
        super().__init__(items)
        self._next_id = 0

    @property
    def model_class(self) -> Type[News]:
        return News

    async def _create_model(self, form: NewsCreateForm, new_id: int) -> News:
        return News(
            id=new_id,
            title=form.title,
            text=form.text
        )

    async def _update_model(self, model: News, form: NewsUpdateForm) -> News:
        model.title = form.title
        model.text = form.text
        return model

    async def _generate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _get_id_filter_specification(self, item_id: int) -> SpecificationInterface[News, bool]:
        return AttributeSpecification('id', item_id, Operator.E)


class ListBasedUserRepository(
    ListBasedCrudRepository[User, int, UserCreateForm, UserUpdateForm],
    UserRepositoryInterface,
):
    _next_id: int

    def __init__(self, items: Optional[List[User]] = None):
        super().__init__(items)
        self._next_id = 0

    def get_by_username(self, username: str) -> User:
        items = self.get_collection(AttributeSpecification('username', username))
        if len(items) == 0:
            raise ItemNotFoundException(User)

        return items[0]

    @property
    def model_class(self) -> Type[User]:
        return User

    def _create_model(self, form: UserCreateForm, new_id: int) -> User:
        if self._username_exists(form.username):
            raise UniqueViolationException(User, 'create', form)

        return User(
            id=new_id,
            username=form.username,
            password=form.password,
            display_name=form.display_name,
        )

    def _update_model(self, model: User, form: UserUpdateForm) -> User:
        model.display_name = form.display_name
        return model

    def _username_exists(self, username: str) -> bool:
        return self.count(AttributeSpecification('username', username)) > 0

    def _generate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _get_id_filter_specification(self, item_id: int) -> SpecificationInterface[User, bool]:
        return AttributeSpecification('id', item_id, Operator.E)


class AsyncListBasedUserRepository(
    AsyncListBasedCrudRepository[User, int, UserCreateForm, UserUpdateForm],
    AsyncUserRepositoryInterface,
):
    _next_id: int

    def __init__(self, items: Optional[List[User]] = None):
        super().__init__(items)
        self._next_id = 0

    async def get_by_username(self, username: str) -> User:
        items = await self.get_collection(AttributeSpecification('username', username))
        if len(items) == 0:
            raise ItemNotFoundException(User)

        return items[0]

    @property
    def model_class(self) -> Type[User]:
        return User

    async def _create_model(self, form: UserCreateForm, new_id: int) -> User:
        if await self._username_exists(form.username):
            raise UniqueViolationException(User, 'create', form)

        return User(
            id=new_id,
            username=form.username,
            password=form.password,
            display_name=form.display_name,
        )

    async def _update_model(self, model: User, form: UserUpdateForm) -> User:
        model.display_name = form.display_name
        return model

    async def _username_exists(self, username: str) -> bool:
        count = await self.count(AttributeSpecification('username', username))
        return count > 0

    async def _generate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _get_id_filter_specification(self, item_id: int) -> SpecificationInterface[User, bool]:
        return AttributeSpecification('id', item_id, Operator.E)
