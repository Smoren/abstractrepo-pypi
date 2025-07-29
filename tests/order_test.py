import pickle
from typing import Tuple, List

import pytest

from abstractrepo.order import OrderOptions
from tests.fixtures.classes import ListBasedNewsRepository, News
from tests.providers.order import data_provider_for_news_order


@pytest.mark.parametrize("test_case", data_provider_for_news_order())
def test_order(test_case: Tuple[List[News], OrderOptions, List[News]]):
    input_news, order_options, expected = test_case
    repo = ListBasedNewsRepository(input_news)
    actual = repo.get_collection(order_options=order_options)
    assert pickle.dumps(actual) == pickle.dumps(expected)
