import pickle
from typing import Tuple, List

import pytest

from abstractrepo.specification import SpecificationInterface
from tests.fixtures.classes import ListBasedNewsRepository, News
from tests.fixtures.providers import data_provider_for_news_repo, data_provider_for_news_filter


@pytest.mark.parametrize("repo", data_provider_for_news_repo())
@pytest.mark.parametrize("test_case", data_provider_for_news_filter())
def test_filters(repo: ListBasedNewsRepository, test_case: Tuple[SpecificationInterface[News, bool], List[News]]):
    filter_spec, expected = test_case
    actual = repo.get_list(filter_spec=filter_spec)
    assert pickle.dumps(actual) == pickle.dumps(expected)
