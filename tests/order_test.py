import pickle
from typing import Tuple, List

import pytest

from abstractrepo.order import OrderOptions
from tests.fixtures.classes import ListBasedNewsRepository, News
from tests.providers.common import data_provider_for_news_repo
from tests.providers.order import data_provider_for_news_order


@pytest.mark.parametrize("repo", data_provider_for_news_repo(5, with_no_text_item=True))
@pytest.mark.parametrize("test_case", data_provider_for_news_order())
def test_filter(repo: ListBasedNewsRepository, test_case: Tuple[OrderOptions, List[News]]):
    order_options, expected = test_case
    actual = repo.get_collection(order_options=order_options)
    assert pickle.dumps(actual) == pickle.dumps(expected)
