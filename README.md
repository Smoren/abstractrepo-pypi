# AbstractRepo - Python Repository Pattern Implementation

[![PyPI package](https://img.shields.io/badge/pip%20install-abstractrepo-brightgreen)](https://pypi.org/project/abstractrepo/)
[![version number](https://img.shields.io/pypi/v/abstractrepo?color=green&label=version)](https://github.com/Smoren/abstractrepo-pypi/releases)
[![Coverage Status](https://coveralls.io/repos/github/Smoren/abstractrepo-pypi/badge.svg?branch=master)](https://coveralls.io/github/Smoren/abstractrepo-pypi?branch=master)
[![Actions Status](https://github.com/Smoren/abstractrepo-pypi/workflows/Test/badge.svg)](https://github.com/Smoren/abstractrepo-pypi/actions)
[![License](https://img.shields.io/github/license/Smoren/abstractrepo-pypi)](https://github.com/Smoren/abstractrepo-pypi/blob/master/LICENSE)

The Abstract Repository library provides a flexible abstraction layer between your application code and data storage systems. 
It implements the repository pattern with support for CRUD operations, filtering using specifications, ordering, pagination, and exception handling. 
This design allows you to easily switch between different persistence mechanisms while maintaining clean separation of concerns in your application architecture.

## Core Concepts
- **CRUD Operations:** Standard Create, Read, Update, Delete functionality
- **Specifications Pattern:** Flexible filtering mechanism based on business rules
- **Ordering Options:** Customizable sorting with control over NULL values placement
- **Pagination Support:** Limit and offset-based page navigation
- **Strong Typing:** Uses Python's typing module for robustness
- **Extensibility:** Designed for easy extension to various database technologies
- **In-Memory Implementation:** Built-in list-based repository for testing/development

## Installation
```bash
pip install abstractrepo
```

## Core Components

### 1. Repository Interface

```python3
import abc
from abstractrepo.repo import CrudRepositoryInterface


class UserRepositoryInterface(CrudRepositoryInterface[User, int, UserCreateSchema, UserUpdateSchema], abc.ABC):  # TModel, TIdValue, TCreateSchema, TUpdateSchema
    pass


class UserRepository(UserRepositoryInterface):
  # Implement abstract methods
  ...
```

**Key Methods:**
- `get_collection()`: Retrieve items with filtering/sorting/pagination
- `count()`: Get filtered item count
- `get_item()`: Get single item by ID
- `exists()`: Check if item exists
- `create()`: Add new item
- `update()`: Modify existing item
- `delete()`: Remove item

### 2. List-Based Implementation
```python
import abc
from typing import Optional, List
from abstractrepo.repo import CrudRepositoryInterface, ListBasedCrudRepository
from abstractrepo.specification import SpecificationInterface, AttributeSpecification, Operator
from abstractrepo.order import OrderOptions
from abstractrepo.paging import PagingOptions


class UserRepositoryInterface(CrudRepositoryInterface[User, int, UserCreateSchema, UserUpdateSchema], abc.ABC):
    pass


class ListBasedNewsRepository(
    ListBasedCrudRepository[User, int, UserCreateSchema, UserUpdateSchema],
    UserRepositoryInterface,
):
    _next_id: int

    def __init__(self, items: Optional[List[User]] = None):
        super().__init__(items)
        self._next_id = 0

    @property
    def model_class(self) -> Type[User]:
        return User

    def _create_model(self, form: UserCreateForm, new_id: int) -> User:
        return User(
            id=new_id,
            username=form.username,
            password=form.password,
            display_name=form.display_name,
        )

    def _update_model(self, model: User, form: UserUpdateForm) -> User:
        model.display_name = form.display_name
        return model

    def _generate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _get_id_filter_specification(self, item_id: int) -> SpecificationInterface[User, bool]:
        return AttributeSpecification('id', item_id, Operator.E)
```

### 3. Specifications
**Filtering with Specifications:**
```python
from abstractrepo.specification import AttributeSpecification, AndSpecification, OrSpecification, Operator

# Single attribute
active_users = AttributeSpecification("is_active", True)

# Complex filters
premium_filter = AndSpecification(
    AttributeSpecification("plan", "premium"),
    OrSpecification(
        AttributeSpecification("age", 30, Operator.GTE),
        AttributeSpecification("join_date", "2023-01-01", Operator.GT)
    )
)
```

**Supported Operators:**
```python
from abstractrepo.specification import Operator

Operator.E          # Equal
Operator.NE         # Not Equal
Operator.GT         # Greater Than
Operator.LT         # Less Than
Operator.GTE        # Greater Than or Equal
Operator.LTE        # Less Than or Equal
Operator.LIKE       # Case-Sensitive Pattern Match
Operator.ILIKE      # Case-Insensitive Pattern Match
Operator.IN         # In List
Operator.NOT_IN     # Not In List
```

### 4. Ordering
```python
from abstractrepo.order import OrderOptionsBuilder, OrderOptions, OrderOption, OrderDirection, NonesOrder

# Single field ordering
ordering = OrderOptions(
    OrderOption("name", OrderDirection.ASC, NonesOrder.LAST)
)

# Multi-field ordering
ordering = OrderOptionsBuilder() \
    .add("priority", OrderDirection.DESC) \
    .add("created_at", OrderDirection.ASC, NonesOrder.LAST) \
    .build()
```

### 5. Pagination
```python
from abstractrepo.paging import PagingOptions, PageResolver

# Manual paging
paging = PagingOptions(limit=10, offset=20)

# Page-based resolver
resolver = PageResolver(page_size=25)
page3 = resolver.get_page(3)
```

### 6. Exceptions
```python
from abstractrepo.exceptions import (
    ItemNotFoundException,
    UniqueViolationException,
    RelationViolationException,
)

try:
    repo.get_item(999)
except ItemNotFoundException as e:
    print(f"Error: {e}")
```

## Complete Example

```python
from abstractrepo.repo import ListBasedCrudRepository
from abstractrepo.specification import AttributeSpecification, Operator
from abstractrepo.order import OrderOptions, OrderOption, OrderDirection
from abstractrepo.paging import PagingOptions

class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

      
class UserRepository(ListBasedCrudRepository[User, int, dict, dict]):
    # Implementation of abstract methods
    ...


# Initialize repository
repo = UserRepository()

# Create users
repo.create({"name": "Alice", "email": "alice@example.com"})
repo.create({"name": "Bob", "email": "bob@example.com"})

# Query with specifications
b_users = repo.get_collection(
    filter_spec=AttributeSpecification("name", "B%", Operator.LIKE),
    order_options=OrderOptions(OrderOption("email", OrderDirection.ASC)),
    paging_options=PagingOptions(limit=5)
)

# Get count
active_count = repo.count(filter_spec=AttributeSpecification("is_active", True))
```

## API Reference

### Repository Methods
| Method           | Parameters                                       | Returns        | Description                          |
|------------------|--------------------------------------------------|----------------|--------------------------------------|
| `get_collection` | `filter_spec`, `order_options`, `paging_options` | `List[TModel]` | Get filtered/sorted/paged collection |
| `count`          | `filter_spec`                                    | `int`          | Count filtered items                 |
| `get_item`       | `item_id`                                        | `TModel`       | Get single item by ID                |
| `exists`         | `item_id`                                        | `bool`         | Check item existence                 |
| `create`         | `form`                                           | `TModel`       | Create new item                      |
| `update`         | `item_id`, `form`                                | `TModel`       | Update existing item                 |
| `delete`         | `item_id`                                        | `TModel`       | Delete item                          |

### Specification Types
| Class                    | Description               |
|--------------------------|---------------------------|
| `AttributeSpecification` | Filter by model attribute |
| `AndSpecification`       | Logical AND combination   |
| `OrSpecification`        | Logical OR combination    |
| `NotSpecification`       | Logical negation          |

### Ordering Options
```
OrderOption(
    attribute: str,
    direction: OrderDirection = OrderDirection.ASC,
    nones: NonesOrder = NonesOrder.FIRST,
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
1. **Type Safety**: Leverage Python's typing system for robust implementations
2. **Specification Composition**: Combine simple specs for complex queries
3. **Null Handling**: Explicitly define null ordering behavior
4. **Pagination**: Use `PageResolver` for consistent page-based navigation
5. **Error Handling**: Catch repository-specific exceptions

## Dependencies
- Python 3.7+
- No external dependencies
