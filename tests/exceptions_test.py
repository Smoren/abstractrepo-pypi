from abstractrepo.exceptions import RelationViolationException, UniqueViolationException, ItemNotFoundException
from abstractrepo.specification import AttributeSpecification
from tests.fixtures.classes import User


def test_item_not_found_exception():
    try:
        raise ItemNotFoundException(User)
    except ItemNotFoundException as e:
        assert str(e) == 'Item of type User not found'
        assert e.cls == User
        assert e.item_id is None

    try:
        raise ItemNotFoundException(User, 42)
    except ItemNotFoundException as e:
        assert str(e) == 'Item of type User not found'
        assert e.cls == User
        assert e.item_id == 42

    specification = AttributeSpecification('id', 42)
    try:
        raise ItemNotFoundException(User, specification=specification)
    except ItemNotFoundException as e:
        assert str(e) == 'Item of type User not found'
        assert e.cls == User
        assert e.item_id is None
        assert e.specification == specification


def test_unique_violation_exception():
    try:
        raise UniqueViolationException(User, 'create', {'username': 'test'})
    except UniqueViolationException as e:
        assert str(e) == 'Action create of User instance failed due to unique violation'
        assert e.cls == User
        assert e.action == 'create'
        assert e.form == {'username': 'test'}


def test_relation_violation_exception():
    try:
        raise RelationViolationException(User, 'update', {'username': 'test'})
    except RelationViolationException as e:
        assert str(e) == 'Action update of User instance failed due to relation violation'
        assert e.cls == User
        assert e.action == 'update'
        assert e.form == {'username': 'test'}
