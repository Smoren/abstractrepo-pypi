from typing import Generator, Tuple, List

from abstractrepo.order import OrderOptions, OrderOptionsBuilder, OrderDirection, NonesOrder
from tests.fixtures.models import News


def data_provider_for_news_order() -> Generator[Tuple[List[News], OrderOptions, List[News]], None, None]:
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('id', OrderDirection.ASC).build(),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
    )
    yield (
        [
            News(id=2, title='Title 2', text='Text 2'),
            News(id=1, title='Title 1', text='Text 1'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('id', OrderDirection.ASC).build(),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
    )
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('id', OrderDirection.DESC).build(),
        [
            News(id=5, title='Title for None text', text=None),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=1, title='Title 1', text='Text 1'),
        ],
    )
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('title', OrderDirection.ASC).build(),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
    )
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('title', OrderDirection.DESC).build(),
        [
            News(id=5, title='Title for None text', text=None),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=1, title='Title 1', text='Text 1'),
        ],
    )
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('text', OrderDirection.ASC, NonesOrder.FIRST).build(),
        [
            News(id=5, title='Title for None text', text=None),
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
        ],
    )
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('text', OrderDirection.ASC, NonesOrder.LAST).build(),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
    )
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('text', OrderDirection.DESC, NonesOrder.FIRST).build(),
        [
            News(id=5, title='Title for None text', text=None),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=1, title='Title 1', text='Text 1'),
        ],
    )
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add('text', OrderDirection.DESC, NonesOrder.LAST).build(),
        [
            News(id=4, title='Title 4', text='Text 4'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=1, title='Title 1', text='Text 1'),
            News(id=5, title='Title for None text', text=None),
        ],
    )
    yield (
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
        OrderOptionsBuilder().add_mass(('id', OrderDirection.ASC), ('title', OrderDirection.ASC, NonesOrder.FIRST)).build(),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title for None text', text=None),
        ],
    )
