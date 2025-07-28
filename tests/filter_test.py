import pickle
from typing import Tuple, List

import pytest

from abstractrepo.specification import SpecificationInterface, AttributeSpecification, Operator
from tests.fixtures.classes import ListBasedNewsRepository, News
from tests.providers.filter import data_provider_for_news_filter, data_provider_for_news_repo


@pytest.mark.parametrize("repo", data_provider_for_news_repo(101, with_no_text_item=True))
@pytest.mark.parametrize("test_case", data_provider_for_news_filter())
def test_filter(repo: ListBasedNewsRepository, test_case: Tuple[SpecificationInterface[News, bool], List[News]]):
    filter_spec, expected = test_case
    actual = repo.get_collection(filter_spec=filter_spec)
    actual_count = repo.count(filter_spec=filter_spec)
    assert pickle.dumps(actual) == pickle.dumps(expected)
    assert actual_count == len(expected)


@pytest.mark.parametrize("repo", data_provider_for_news_repo(100))
def test_filter_errors(repo: ListBasedNewsRepository):
    with pytest.raises(ValueError):
        repo.get_collection(AttributeSpecification('id', 12, Operator.IN))

    with pytest.raises(ValueError):
        repo.get_collection(AttributeSpecification('id', 12, Operator.NOT_IN))

    with pytest.raises(TypeError):
        repo.get_collection(AttributeSpecification('id', 12, 'UnsupportedOperator'))
