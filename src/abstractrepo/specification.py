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
    """Enumeration of comparison operators used in specifications.

    This enum defines the various comparison operators that can be used
    when creating attribute-based specifications for filtering data.
    """
    E = '='            # Equal
    NE = '!='          # Not Equal
    GT = '>'           # Greater Than
    LT = '<'           # Less Than
    GTE = '>='         # Greater Than or Equal
    LTE = '<='         # Less Than or Equal
    LIKE = 'LIKE'      # SQL-like pattern matching (case-sensitive)
    ILIKE = 'ILIKE'    # SQL-like pattern matching (case-insensitive)
    IN = 'IN'          # Value is in a list
    NOT_IN = 'NOT_IN'  # Value is not in a list


class SpecificationInterface(Generic[TModel, TResult], abc.ABC):
    """Abstract base class for all specifications.

    A specification encapsulates business rules and criteria that can be applied
    to models to determine if they satisfy certain conditions. This follows the
    Specification Pattern, which allows for composable and reusable business logic.

    Type Parameters:
        TModel: The type of model this specification can evaluate.
        TResult: The type of result returned by the specification evaluation.
    """
    @abc.abstractmethod
    def is_satisfied_by(self, model: TModel) -> TResult:
        """Evaluates whether the given model satisfies this specification.

        Args:
            model: The model instance to evaluate against this specification.

        Returns:
            The result of the specification evaluation (typically boolean).
        """
        raise NotImplementedError()


class SpecificationConverterInterface(Generic[TModelFrom, TResultFrom, TModelTo, TResultTo], abc.ABC):
    """Abstract base class for converting specifications between different model types.

    This interface defines a method for converting a specification from one model type
    and result type to another. This is useful when you have a generic specification
    that needs to be adapted for a specific data source or model representation.

    Type Parameters:
        TModelFrom: The original model type of the specification.
        TResultFrom: The original result type of the specification.
        TModelTo: The target model type for the converted specification.
        TResultTo: The target result type for the converted specification.
    """
    @abc.abstractmethod
    def convert(
        self,
        specification: SpecificationInterface[TModelFrom, TResultFrom],
    ) -> SpecificationInterface[TModelTo, TResultTo]:
        """Converts a given specification from one model/result type to another.

        Args:
            specification: The original specification to convert.

        Returns:
            A new SpecificationInterface instance for the target model/result types.
        """
        raise NotImplementedError()


class BaseAndSpecification(Generic[TModel, TResult], SpecificationInterface[TModel, TResult], abc.ABC):
    """Base abstract class for AND logical specifications.

    This class represents a composite specification where all contained specifications
    must be satisfied for this specification to be satisfied. It serves as a base
    for concrete AND implementations.

    Attributes:
        specifications: A list of SpecificationInterface instances to be combined with AND logic.

    Type Parameters:
        TModel: The type of model this specification can evaluate.
        TResult: The type of result returned by the specification evaluation.
    """
    specifications: List[SpecificationInterface[TModel, TResult]]

    def __init__(self, *specifications: SpecificationInterface[TModel, TResult]):
        """Initializes a new BaseAndSpecification.

        Args:
            *specifications: One or more SpecificationInterface instances to combine.
        """
        self.specifications = list(specifications)


class BaseOrSpecification(Generic[TModel, TResult], SpecificationInterface[TModel, TResult], abc.ABC):
    """Base abstract class for OR logical specifications.

    This class represents a composite specification where at least one of the
    contained specifications must be satisfied for this specification to be satisfied.
    It serves as a base for concrete OR implementations.

    Attributes:
        specifications: A list of SpecificationInterface instances to be combined with OR logic.

    Type Parameters:
        TModel: The type of model this specification can evaluate.
        TResult: The type of result returned by the specification evaluation.
    """
    specifications: List[SpecificationInterface[TModel, TResult]]

    def __init__(self, *specifications: SpecificationInterface[TModel, TResult]):
        """Initializes a new BaseOrSpecification.

        Args:
            *specifications: One or more SpecificationInterface instances to combine.
        """
        self.specifications = list(specifications)


class BaseNotSpecification(Generic[TModel, TResult], SpecificationInterface[TModel, TResult], abc.ABC):
    """Base abstract class for NOT logical specifications.

    This class represents a composite specification that negates the result of
    another specification. It serves as a base for concrete NOT implementations.

    Attributes:
        specification: The SpecificationInterface instance to be negated.

    Type Parameters:
        TModel: The type of model this specification can evaluate.
        TResult: The type of result returned by the specification evaluation.
    """
    specification: SpecificationInterface[TModel, TResult]

    def __init__(self, specification: SpecificationInterface[TModel, TResult]):
        """Initializes a new BaseNotSpecification.

        Args:
            specification: The SpecificationInterface instance to negate.
        """
        self.specification = specification


class BaseAttributeSpecification(Generic[TModel, TResult], SpecificationInterface[TModel, TResult], abc.ABC):
    """Base abstract class for attribute-based specifications.

    This class represents a specification that evaluates a model based on the value
    of a specific attribute and a given operator. It serves as a base for concrete
    attribute-based implementations.

    Attributes:
        attribute_name: The name of the attribute to evaluate.
        attribute_value: The value to compare against the attribute's value.
        operator: The comparison operator to use (e.g., equality, greater than).

    Type Parameters:
        TModel: The type of model this specification can evaluate.
        TResult: The type of result returned by the specification evaluation.
    """
    attribute_name: str
    attribute_value: object
    operator: Operator

    def __init__(self, attribute_name: str, attribute_value: object, operator: Operator = Operator.E):
        """Initializes a new BaseAttributeSpecification.

        Args:
            attribute_name: The name of the attribute on the model to check.
            attribute_value: The value to compare against the attribute.
            operator: The comparison operator to use. Defaults to Operator.E (equality).
        """
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.operator = operator


class AndSpecification(Generic[TModel], BaseAndSpecification[TModel, bool]):
    """A concrete implementation of an AND logical specification.

    This specification is satisfied only if all its contained specifications are satisfied.
    """
    def is_satisfied_by(self, model: TModel) -> bool:
        """Checks if all contained specifications are satisfied by the model.

        Args:
            model: The model instance to evaluate.

        Returns:
            True if all specifications are satisfied, False otherwise.
        """
        for specification in self.specifications:
            if not specification.is_satisfied_by(model):
                return False
        return True


class OrSpecification(Generic[TModel], BaseOrSpecification[TModel, bool]):
    """A concrete implementation of an OR logical specification.

    This specification is satisfied if at least one of its contained specifications is satisfied.
    """
    def is_satisfied_by(self, model: TModel) -> bool:
        """Checks if at least one contained specification is satisfied by the model.

        Args:
            model: The model instance to evaluate.

        Returns:
            True if any specification is satisfied, False otherwise.
        """
        for specification in self.specifications:
            if specification.is_satisfied_by(model):
                return True
        return False


class NotSpecification(Generic[TModel], BaseNotSpecification[TModel, bool]):
    """A concrete implementation of a NOT logical specification.

    This specification negates the result of its contained specification.
    """
    def is_satisfied_by(self, model: TModel) -> bool:
        """Checks if the contained specification is NOT satisfied by the model.

        Args:
            model: The model instance to evaluate.

        Returns:
            True if the contained specification is not satisfied, False otherwise.
        """
        return not self.specification.is_satisfied_by(model)


class AttributeSpecification(Generic[TModel], BaseAttributeSpecification[TModel, bool]):
    """A concrete implementation of an attribute-based specification.

    This specification evaluates a model based on the value of a specific attribute
    and a given comparison operator.
    """
    def is_satisfied_by(self, model: TModel) -> bool:
        """Checks if the model's attribute satisfies the condition defined by the operator and value.

        Args:
            model: The model instance to evaluate.

        Returns:
            True if the attribute satisfies the condition, False otherwise.

        Raises:
            ValueError: If the attribute value type is not compatible with the operator (e.g., IN/NOT_IN with non-list).
            TypeError: If an unsupported operator is provided.
        """
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
            return self._like(str(self.attribute_value), model_attr)
        if self.operator == Operator.ILIKE:
            return self._like(str(self.attribute_value).lower(), model_attr.lower())
        if self.operator == Operator.IN:
            if isinstance(self.attribute_value, list):
                return model_attr in self.attribute_value
            raise ValueError('Attribute value must be a list')
        if self.operator == Operator.NOT_IN:
            if isinstance(self.attribute_value, list):
                return model_attr not in self.attribute_value
            raise ValueError('Attribute value must be a list')
        raise TypeError(f'Unsupported operator: {self.operator}')

    @staticmethod
    def _like(pattern: str, string: str) -> bool:
        """Helper method for LIKE and ILIKE operations.

        Performs a SQL-like pattern match on the given string.
        """
        # Replace SQL pattern wildcards (%) and (_) with regex equivalents
        pattern = pattern.replace('%', '.*').replace('_', '.')
        # Add start and end of string
        pattern = '^' + pattern + '$'
        # Check if the string matches the pattern
        return re.match(pattern, string) is not None
