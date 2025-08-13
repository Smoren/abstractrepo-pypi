# AbstractRepo - Python Repository Pattern Implementation

[![PyPI package](https://img.shields.io/badge/pip%20install-abstractrepo-brightgreen)](https://pypi.org/project/abstractrepo/)
[![version number](https://img.shields.io/pypi/v/abstractrepo?color=green&label=version)](https://github.com/Smoren/abstractrepo-pypi/releases)
[![Coverage Status](https://coveralls.io/repos/github/Smoren/abstractrepo-pypi/badge.svg?branch=master)](https://coveralls.io/github/Smoren/abstractrepo-pypi?branch=master)
[![Actions Status](https://github.com/Smoren/abstractrepo-pypi/workflows/Test/badge.svg)](https://github.com/Smoren/abstractrepo-pypi/actions)
[![License](https://img.shields.io/github/license/Smoren/abstractrepo-pypi)](https://github.com/Smoren/abstractrepo-pypi/blob/master/LICENSE)

The `AbstractRepo` library provides a robust and flexible abstraction layer for interacting with various data storage systems in Python. It implements the widely recognized Repository Pattern, offering a clean and consistent API for common data operations such as Create, Read, Update, and Delete (CRUD). This design promotes a clear separation of concerns, making your application logic independent of the underlying data persistence mechanism. This allows for easy switching between different databases or storage solutions without significant changes to your core business logic.

## Key Features

* **CRUD Operations:** Comprehensive support for standard data manipulation operations.
* **Specifications Pattern:** A powerful and flexible mechanism for defining complex query criteria based on business rules, enabling highly customizable data retrieval.
* **Ordering Options:** Advanced sorting capabilities, including control over the placement of `NULL` values.
* **Pagination Support:** Efficient handling of large datasets through limit and offset-based pagination.
* **Strong Typing:** Leverages Python's type hinting for improved code readability, maintainability, and early error detection.
* **Extensibility:** Designed with extensibility in mind, allowing for easy integration with various database technologies and custom data sources.
* **In-Memory Implementation:** Includes a built-in list-based repository implementation, ideal for testing, development, and rapid prototyping.
* **Asynchronous Support:** Provides interfaces and base implementations for asynchronous repository operations, crucial for modern, high-performance applications.

## Installation

To get started with `AbstractRepo`, install it using pip:

```shell
pip install abstractrepo
```

## Table of Contents

* [Core Components and Usage](#core-components-and-usage)
  * [Repository Interface (`CrudRepositoryInterface`)](#repository-interface-crudrepositoryinterface)
  * [List-Based Implementation (`ListBasedCrudRepository`)](#list-based-implementation-listbasedcrudrepository)
  * [Asynchronous Repositories (`AsyncCrudRepositoryInterface`)](#asynchronous-repositories)
  * [Specifications](#specifications)
  * [Ordering](#ordering)
  * [Pagination](#pagination)
  * [Exception Handling](#exception-handling)
* [Examples](#examples)
  * [Complete Synchronous Example](#complete-synchronous-example)
  * [Complete Asynchronous Example](#complete-asynchronous-example)
* [API Reference](#api-reference)
  * [Repository Methods](#repository-methods)
  * [Specification Types](#specification-types)
  * [Ordering Options](#ordering-options)
  * [Pagination Options](#pagination-options)
* [Best Practices](#best-practices)
* [Dependencies](#dependencies)
* [License](#license)

## Core Components and Usage

### Repository Interface (`CrudRepositoryInterface`)

The `CrudRepositoryInterface` defines the contract for all synchronous repositories. It specifies the standard CRUD operations and other essential methods that any concrete repository implementation must adhere to.

```python
import abc
from pydantic import BaseModel
from abstractrepo.repo import CrudRepositoryInterface


class User(BaseModel):
    id: int
    username: str
    password: str
    display_name: str

class UserCreateForm(BaseModel):
    username: str
    password: str
    display_name: str

class UserUpdateForm(BaseModel):
    display_name: str


class UserRepositoryInterface(CrudRepositoryInterface[User, int, UserCreateForm, UserUpdateForm], abc.ABC):
    pass


class UserRepository(UserRepositoryInterface):
    # Implement abstract methods here
    ...
```

**Key Methods:**

| Method           | Parameters                                       | Returns        | Description                                                                                    |
|:-----------------|:-------------------------------------------------|:---------------|:-----------------------------------------------------------------------------------------------|
| `get_collection` | `filter_spec`, `order_options`, `paging_options` | `List[TModel]` | Retrieves a collection of items based on filtering, sorting, and pagination options.           |
| `count`          | `filter_spec`                                    | `int`          | Returns the total count of items matching the given filter specification.                      |
| `get_item`       | `item_id`                                        | `TModel`       | Retrieves a single item by its unique identifier. Raises `ItemNotFoundException` if not found. |
| `exists`         | `item_id`                                        | `bool`         | Checks if an item with the specified ID exists in the repository.                              |
| `create`         | `form`                                           | `TModel`       | Creates a new item in the repository using the provided creation form.                         |
| `update`         | `item_id`, `form`                                | `TModel`       | Updates an existing item identified by its ID with data from the update form.                  |
| `delete`         | `item_id`                                        | `TModel`       | Deletes an item from the repository by its ID.                                                 |
| `model_class`    | (Property)                                       | `Type[TModel]` | Returns the model class associated with the repository.                                        |

### List-Based Implementation (`ListBasedCrudRepository`)

The `ListBasedCrudRepository` provides a concrete, in-memory implementation of the `CrudRepositoryInterface`. It's particularly useful for testing, development, and scenarios where a simple, non-persistent data store is sufficient.

```python
import abc
from typing import Optional, List, Type
from pydantic import BaseModel
from abstractrepo.repo import CrudRepositoryInterface, ListBasedCrudRepository
from abstractrepo.specification import SpecificationInterface, AttributeSpecification, Operator
from abstractrepo.exceptions import ItemNotFoundException, UniqueViolationException


class User(BaseModel):
    id: int
    username: str
    password: str
    display_name: str

class UserCreateForm(BaseModel):
    username: str
    password: str
    display_name: str

class UserUpdateForm(BaseModel):
    display_name: str


class UserRepositoryInterface(CrudRepositoryInterface[User, int, UserCreateForm, UserUpdateForm], abc.ABC):
    pass


class ListBasedUserRepository(
    ListBasedCrudRepository[User, int, UserCreateForm, UserUpdateForm],
    UserRepositoryInterface,
):
    _next_id: int

    def __init__(self, items: Optional[List[User]] = None):
        super().__init__(items)
        self._next_id = 0

    def get_by_username(self, username: str) -> User:
        items = self.get_collection(AttributeSpecification("username", username))
        if len(items) == 0:
            raise ItemNotFoundException(User)

        return items[0]

    @property
    def model_class(self) -> Type[User]:
        return User

    def _create_model(self, form: UserCreateForm, new_id: int) -> User:
        if self._username_exists(form.username):
            raise UniqueViolationException(User, "create", form)

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
        return self.count(AttributeSpecification("username", username)) > 0

    def _generate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _get_id_filter_specification(self, item_id: int) -> SpecificationInterface[User, bool]:
        return AttributeSpecification("id", item_id, Operator.E)
```

### Asynchronous Repositories

`AbstractRepo` provides full support for asynchronous operations, allowing you to build non-blocking data access layers for high-performance applications. The `AsyncCrudRepositoryInterface` defines the asynchronous contract, and `AsyncListBasedCrudRepository` offers an in-memory asynchronous implementation.

This interface mirrors the synchronous `CrudRepositoryInterface` but with `async` methods, enabling seamless integration with `asyncio` and other asynchronous frameworks.

```python
import abc
from typing import TypeVar
from pydantic import BaseModel
from abstractrepo.repo import AsyncCrudRepositoryInterface


class User(BaseModel):
    id: int
    username: str
    password: str
    display_name: str

class UserCreateForm(BaseModel):
    username: str
    password: str
    display_name: str

class UserUpdateForm(BaseModel):
    display_name: str


class AsyncUserRepositoryInterface(AsyncCrudRepositoryInterface[User, int, UserCreateForm, UserUpdateForm], abc.ABC):
    pass


class AsyncUserRepository(AsyncUserRepositoryInterface):
    # Implement abstract async methods here
    ...
```

### Specifications

The Specifications Pattern allows you to define flexible and reusable filtering logic. You can combine simple specifications to build complex queries.

**Filtering with Specifications:**

```python
from abstractrepo.specification import AttributeSpecification, AndSpecification, OrSpecification, Operator

# Single attribute filter
active_users_spec = AttributeSpecification("is_active", True)

# Complex filter combining AND and OR operations
premium_filter_spec = AndSpecification(
    AttributeSpecification("plan", "premium"),
    OrSpecification(
        AttributeSpecification("age", 30, Operator.GTE),
        AttributeSpecification("join_date", "2023-01-01", Operator.GT)
    )
)
```

**Supported Operators:**

`AbstractRepo` provides a rich set of operators for various comparison and matching needs:

| Operator | Description                    |
| :------- |:-------------------------------|
| `E`      | Equal                          |
| `NE`     | Not Equal                      |
| `GT`     | Greater Than                   |
| `LT`     | Less Than                      |
| `GTE`    | Greater Than or Equal          |
| `LTE`    | Less Than or Equal             |
| `LIKE`   | Case-Sensitive Pattern Match   |
| `ILIKE`  | Case-Insensitive Pattern Match |
| `IN`     | In List                        |
| `NOT_IN` | Not In List                    |

### Ordering

Control the order of retrieved items using `OrderOptions` and `OrderOption`. You can specify the attribute to sort by, the direction (ascending or descending), and how `None` values should be handled.

```python
from abstractrepo.order import OrderOptionsBuilder, OrderOptions, OrderOption, OrderDirection, NonesOrder

# Single field ordering
ordering_by_name = OrderOptions(
    OrderOption("name", OrderDirection.ASC, NonesOrder.LAST)
)

# Multi-field ordering using OrderOptionsBuilder for chaining
complex_ordering = OrderOptionsBuilder() \
    .add("priority", OrderDirection.DESC) \
    .add("created_at", OrderDirection.ASC, NonesOrder.LAST) \
    .build()
```

### Pagination

Manage large result sets efficiently with `PagingOptions` for limit/offset-based pagination and `PageResolver` for page-number-based navigation.

```python
from abstractrepo.paging import PagingOptions, PageResolver

# Manual paging with limit and offset
manual_paging = PagingOptions(limit=10, offset=20)

# Page-based resolver for consistent page navigation
resolver = PageResolver(page_size=25)
page_3_options = resolver.get_page(3) # Retrieves PagingOptions for the 3rd page
```

### Exception Handling

`AbstractRepo` defines specific exceptions to handle common repository-related errors, allowing for robust error management in your application.

```python
from abstractrepo.exceptions import (
    ItemNotFoundException,
    UniqueViolationException,
    RelationViolationException,
)

try:
    repo.get_item(999) # Attempt to retrieve a non-existent item
except ItemNotFoundException as e:
    print(f"Error: {e}") # Handle the case where the item is not found
```

## Examples

### Complete Synchronous Example

This example demonstrates the full lifecycle of a synchronous repository using the `ListBasedCrudRepository`.

```python
from abstractrepo.repo import ListBasedCrudRepository
from abstractrepo.specification import AttributeSpecification, Operator
from abstractrepo.order import OrderOptions, OrderOption, OrderDirection
from abstractrepo.paging import PagingOptions
from pydantic import BaseModel

# Define your data model
class User(BaseModel):
    id: int
    name: str
    email: str

# Define forms for creation and update (can be pure classes Pydantic models)
class UserCreateForm(BaseModel):
    name: str
    email: str

class UserUpdateForm(BaseModel):
    name: str | None = None
    email: str | None = None

# Implement your concrete repository
class ConcreteUserRepository(ListBasedCrudRepository[User, int, UserCreateForm, UserUpdateForm]):
    _next_id: int = 0

    def __init__(self, items: list[User] | None = None):
        super().__init__(items)
        if items:
            self._next_id = max(item.id for item in items) + 1

    @property
    def model_class(self) -> type[User]:
        return User

    def _create_model(self, form: UserCreateForm, new_id: int) -> User:
        # In a real scenario, you might check for unique constraints here
        return User(id=new_id, name=form.name, email=form.email)

    def _update_model(self, model: User, form: UserUpdateForm) -> User:
        if form.name is not None:
            model.name = form.name
        if form.email is not None:
            model.email = form.email
        return model

    def _generate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _get_id_filter_specification(self, item_id: int) -> AttributeSpecification[User, bool]:
        return AttributeSpecification("id", item_id, Operator.E)


# --- Usage Example ---

# Initialize repository
user_repo = ConcreteUserRepository()

# Create users
alice = user_repo.create(UserCreateForm(name="Alice", email="alice@example.com"))
bob = user_repo.create(UserCreateForm(name="Bob", email="bob@example.com"))
charlie = user_repo.create(UserCreateForm(name="Charlie", email="charlie@example.com"))

print(f"Created users: {alice.name}, {bob.name}, {charlie.name}")

# Query with specifications
b_users = user_repo.get_collection(
    filter_spec=AttributeSpecification("name", "B%", Operator.LIKE),
    order_options=OrderOptions(OrderOption("email", OrderDirection.ASC)),
    paging_options=PagingOptions(limit=5)
)
print(f"Users with name starting with 'B': {[u.name for u in b_users]}")

# Get a single user by ID
retrieved_alice = user_repo.get_item(alice.id)
print(f"Retrieved user by ID: {retrieved_alice.name}")

# Update a user
user_repo.update(bob.id, UserUpdateForm(email="robert@example.com"))
updated_bob = user_repo.get_item(bob.id)
print(f"Updated Bob's email to: {updated_bob.email}")

# Get count
total_users = user_repo.count()
print(f"Total users: {total_users}")

# Delete a user
user_repo.delete(charlie.id)
print(f"Users after deleting Charlie: {[u.name for u in user_repo.get_collection()]}")

# Check existence
print(f"Does Alice exist? {user_repo.exists(alice.id)}")
print(f"Does Charlie exist? {user_repo.exists(charlie.id)}")
```

### Complete Asynchronous Example

This example demonstrates how to implement and use an asynchronous repository with `AsyncListBasedCrudRepository`.

```python
import asyncio
from abstractrepo.repo import AsyncListBasedCrudRepository
from abstractrepo.specification import AttributeSpecification, Operator
from abstractrepo.order import OrderOptions, OrderOption, OrderDirection
from abstractrepo.paging import PagingOptions
from pydantic import BaseModel
from typing import List, Type, Optional

# Define your data model
class User(BaseModel):
    id: int
    name: str
    email: str

# Define forms for creation and update
class UserCreateForm(BaseModel):
    name: str
    email: str

class UserUpdateForm(BaseModel):
    name: str | None = None
    email: str | None = None

# Implement your concrete asynchronous repository
class ConcreteAsyncUserRepository(AsyncListBasedCrudRepository[User, int, UserCreateForm, UserUpdateForm]):
    _next_id: int = 0

    def __init__(self, items: List[User] | None = None):
        super().__init__(items)
        if items:
            self._next_id = max(item.id for item in items) + 1

    @property
    def model_class(self) -> Type[User]:
        return User

    async def _create_model(self, form: UserCreateForm, new_id: int) -> User:
        # Simulate async operation
        await asyncio.sleep(0.01)
        return User(id=new_id, name=form.name, email=form.email)

    async def _update_model(self, model: User, form: UserUpdateForm) -> User:
        # Simulate async operation
        await asyncio.sleep(0.01)
        if form.name is not None:
            model.name = form.name
        if form.email is not None:
            model.email = form.email
        return model

    async def _generate_id(self) -> int:
        # Simulate async operation
        await asyncio.sleep(0.01)
        self._next_id += 1
        return self._next_id

    def _get_id_filter_specification(self, item_id: int) -> AttributeSpecification[User, bool]:
        return AttributeSpecification("id", item_id, Operator.E)


# --- Usage Example ---

async def main():
    # Initialize asynchronous repository
    async_user_repo = ConcreteAsyncUserRepository()

    # Create users asynchronously
    alice = await async_user_repo.create(UserCreateForm(name="Alice", email="alice@example.com"))
    bob = await async_user_repo.create(UserCreateForm(name="Bob", email="bob@example.com"))
    charlie = await async_user_repo.create(UserCreateForm(name="Charlie", email="charlie@example.com"))

    print(f"Created users: {alice.name}, {bob.name}, {charlie.name}")

    # Query with specifications asynchronously
    b_users = await async_user_repo.get_collection(
        filter_spec=AttributeSpecification("name", "B%", Operator.LIKE),
        order_options=OrderOptions(OrderOption("email", OrderDirection.ASC)),
        paging_options=PagingOptions(limit=5)
    )
    print(f"Users with name starting with 'B': {[u.name for u in b_users]}")

    # Get a single user by ID asynchronously
    retrieved_alice = await async_user_repo.get_item(alice.id)
    print(f"Retrieved user by ID: {retrieved_alice.name}")

    # Update a user asynchronously
    await async_user_repo.update(bob.id, UserUpdateForm(email="robert@example.com"))
    updated_bob = await async_user_repo.get_item(bob.id)
    print(f"Updated Bob's email to: {updated_bob.email}")

    # Get count asynchronously
    total_users = await async_user_repo.count()
    print(f"Total users: {total_users}")

    # Delete a user asynchronously
    await async_user_repo.delete(charlie.id)
    users_after_delete = await async_user_repo.get_collection()
    print(f"Users after deleting Charlie: {[u.name for u in users_after_delete]}")

    # Check existence asynchronously
    print(f"Does Alice exist? {await async_user_repo.exists(alice.id)}")
    print(f"Does Charlie exist? {await async_user_repo.exists(charlie.id)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### Repository Methods

| Method           | Parameters                                       | Returns        | Description                          |
|:-----------------|:-------------------------------------------------|:---------------|:-------------------------------------|
| `get_collection` | `filter_spec`, `order_options`, `paging_options` | `List[TModel]` | Get filtered/sorted/paged collection |
| `count`          | `filter_spec`                                    | `int`          | Count filtered items                 |
| `get_item`       | `item_id`                                        | `TModel`       | Get single item by ID                |
| `exists`         | `item_id`                                        | `bool`         | Check item existence                 |
| `create`         | `form`                                           | `TModel`       | Create new item                      |
| `update`         | `item_id`, `form`                                | `TModel`       | Update existing item                 |
| `delete`         | `item_id`                                        | `TModel`       | Delete item                          |

### Specification Types

| Class                    | Description               |
|:-------------------------|:--------------------------|
| `AttributeSpecification` | Filter by model attribute |
| `AndSpecification`       | Logical AND combination   |
| `OrSpecification`        | Logical OR combination    |
| `NotSpecification`       | Logical negation          |

### Ordering Options

```
OrderOption(
    attribute: str,
    direction: OrderDirection = OrderDirection.ASC,
    nones: Optional[NonesOrder] = None,
)
```

### Pagination Options

```
PagingOptions(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
)
```

## Best Practices

1. **Type Safety**: Leverage Python's typing system for robust implementations.
2. **Specification Composition**: Combine simple specs for complex queries.
3. **Null Handling**: Explicitly define null ordering behavior.
4. **Pagination**: Use `PageResolver` for consistent page-based navigation.
5. **Error Handling**: Catch repository-specific exceptions.
6. **Asynchronous Operations**: Use `await` with asynchronous repository methods to ensure non-blocking execution.
7. **Use pydantic for data modeling**: Define your models using pydantic, allowing for robust data validation and auto-generation of CRUD repository methods.

## Dependencies

* Python 3.7+
* No external dependencies

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

