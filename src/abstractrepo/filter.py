import abc
import re
from enum import Enum
from typing import List, TypeVar, Generic

TResult = TypeVar('TResult')
TModel = TypeVar('TModel')

TResultFrom = TypeVar('TResultFrom')
TResultTo = TypeVar('TResultTo')

TModelFrom = TypeVar('TModelFrom')
TModelTo = TypeVar('TModelTo')


class Operator(Enum):
    E = '='
    NE = '!='
    GT = '>'
    LT = '<'
    GTE = '>='
    LTE = '<='
    LIKE = 'LIKE'
    ILIKE = 'ILIKE'
    IN = 'IN'
    NOT_IN = 'NOT_IN'


class SpecificationInterface(Generic[TModel, TResult], abc.ABC):
    @abc.abstractmethod
    def is_satisfied_by(self, model: TModel) -> TResult:
        raise NotImplementedError()


class SpecificationConverterInterface(Generic[TModelFrom, TResultFrom, TModelTo, TResultTo], abc.ABC):
    @abc.abstractmethod
    def convert(
        self,
        specification: SpecificationInterface[TModelFrom, TResultFrom],
    ) -> SpecificationInterface[TModelTo, TResultTo]:
        raise NotImplementedError()


class BaseAndSpecification(Generic[TModel, TResult], SpecificationInterface[TModel, TResult], abc.ABC):
    specifications: List[SpecificationInterface[TModel, TResult]]

    def __init__(self, *specifications: SpecificationInterface[TModel, TResult]):
        self.specifications = list(specifications)


class BaseOrSpecification(Generic[TModel, TResult], SpecificationInterface[TModel, TResult], abc.ABC):
    specifications: List[SpecificationInterface[TModel, TResult]]

    def __init__(self, *specifications: SpecificationInterface[TModel, TResult]):
        self.specifications = list(specifications)


class BaseNotSpecification(Generic[TModel, TResult], SpecificationInterface[TModel, TResult], abc.ABC):
    specification: SpecificationInterface[TModel, TResult]

    def __init__(self, specification: SpecificationInterface[TModel, TResult]):
        self.specification = specification


class BaseAttributeSpecification(Generic[TModel, TResult], SpecificationInterface[TModel, TResult], abc.ABC):
    attribute_name: str
    attribute_value: object
    operator: Operator

    def __init__(self, attribute_name: str, attribute_value: object, operator: Operator = Operator.E):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.operator = operator


class AndSpecification(BaseAndSpecification[object, bool]):
    def is_satisfied_by(self, model: object) -> bool:
        for specification in self.specifications:
            if not specification.is_satisfied_by(model):
                return False
        return True


class OrSpecification(BaseOrSpecification[object, bool]):
    def is_satisfied_by(self, model: object) -> bool:
        for specification in self.specifications:
            if specification.is_satisfied_by(model):
                return True
        return False


class NotSpecification(BaseNotSpecification[object, bool]):
    def is_satisfied_by(self, model: object) -> bool:
        return not self.specification.is_satisfied_by(model)


class AttributeSpecification(BaseAttributeSpecification[object, bool]):
    def is_satisfied_by(self, model: object) -> bool:
        model_attr = getattr(model, self.attribute_name)

        if model_attr is None and self.attribute_value is not None:
            return False

        if self.operator == Operator.E:
            if self.attribute_value is None:
                return model_attr is None
            return model_attr == self.attribute_value
        if self.operator == Operator.NE:
            if self.attribute_value is None:
                return model_attr is not None
            return model_attr != self.attribute_value
        if self.operator == Operator.GT:
            return model_attr > self.attribute_value
        if self.operator == Operator.LT:
            return model_attr < self.attribute_value
        if self.operator == Operator.GTE:
            return model_attr >= self.attribute_value
        if self.operator == Operator.LTE:
            return model_attr <= self.attribute_value
        if self.operator == Operator.LIKE:
            return self.like(str(self.attribute_value), model_attr)
        if self.operator == Operator.ILIKE:
            return self.like(str(self.attribute_value).lower(), model_attr.lower())
        if self.operator == Operator.IN:
            if isinstance(self.attribute_value, list):
                return model_attr in self.attribute_value
            raise ValueError('Attribute value must be a list')
        if self.operator == Operator.NOT_IN:
            if isinstance(self.attribute_value, list):
                return model_attr not in self.attribute_value
            raise ValueError('Attribute value must be a list')
        raise NotImplementedError(f'Unsupported operator: {self.operator}')

    @staticmethod
    def like(pattern: str, string: str) -> bool:
        # Заменить SQL шаблоны (%) и (_) на соответствующие регулярным выражениям
        pattern = pattern.replace('%', '.*').replace('_', '.')
        # Добавить начало и конец строки
        pattern = '^' + pattern + '$'
        # Проверить, соответствует ли строка шаблону
        return re.match(pattern, string) is not None
