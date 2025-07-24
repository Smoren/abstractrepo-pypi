class RepositoryExceptionInterface(Exception):
    pass


class ItemNotFoundException(RepositoryExceptionInterface):
    def __init__(self, cls: type, item_id: int):
        super().__init__(f'Item of type {cls.__name__} with id {item_id} not found')


class UniqueViolationException(RepositoryExceptionInterface):
    def __init__(self, action: str, form: object):
        super().__init__(f'Action {action} failed due to unique violation: {form}')


class RelationViolationException(RepositoryExceptionInterface):
    def __init__(self, action: str, form: object):
        super().__init__(f'Action {action} failed due to relation violation: {form}')
