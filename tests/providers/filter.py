from typing import Generator, Tuple, List

from abstractrepo.specification import SpecificationInterface, AttributeSpecification, Operator, AndSpecification, \
    OrSpecification, NotSpecification
from tests.fixtures.classes import News, ListBasedNewsRepository, NewsCreateForm, NewsRepositoryInterface, \
    AsyncListBasedNewsRepository, AsyncNewsRepositoryInterface


def data_provider_for_news_repo(size: int, with_no_text_item: bool = False) -> Generator[NewsRepositoryInterface, None, None]:
    repo = ListBasedNewsRepository()
    for i in range(size - int(with_no_text_item)):
        repo.create(NewsCreateForm(title=f'Title {i+1}', text=f'Text {i+1}'))

    if with_no_text_item:
        repo.create(NewsCreateForm(title=f'Title for None text', text=None))

    yield repo


def data_provider_for_news_repo_async(size: int, with_no_text_item: bool = False) -> Generator[AsyncNewsRepositoryInterface, None, None]:
    # Helper function to run async generator to completion
    async def collect():
        repo = AsyncListBasedNewsRepository()
        for i in range(size - int(with_no_text_item)):
            await repo.create(NewsCreateForm(title=f'Title {i + 1}', text=f'Text {i + 1}'))

        if with_no_text_item:
            await repo.create(NewsCreateForm(title=f'Title for None text', text=None))

        return [repo]

    # Run the async collection synchronously
    import asyncio
    yield from asyncio.run(collect())


def data_provider_for_news_filter() -> Generator[Tuple[SpecificationInterface[News, bool], List[News]], None, None]:
    yield (
        AttributeSpecification('id', -1, Operator.E),
        [],
    )
    yield (
        AttributeSpecification('id', 1, Operator.E),
        [News(id=1, title='Title 1', text='Text 1')],
    )
    yield (
        AttributeSpecification('title', 'Title 22', Operator.E),
        [News(id=22, title='Title 22', text='Text 22')],
    )
    yield (
        AttributeSpecification('text', 'Text 22', Operator.E),
        [News(id=22, title='Title 22', text='Text 22')],
    )
    yield (
        AttributeSpecification('text', None, Operator.E),
        [News(id=101, title='Title for None text', text=None)],
    )
    yield (
        AttributeSpecification('title', '%for None%', Operator.LIKE),
        [News(id=101, title='Title for None text', text=None)],
    )
    yield (
        AttributeSpecification('title', '%for none%', Operator.LIKE),
        [],
    )
    yield (
        AttributeSpecification('title', '%for none%', Operator.ILIKE),
        [News(id=101, title='Title for None text', text=None)],
    )
    yield (
        AttributeSpecification('title', '%for 111%', Operator.ILIKE),
        [],
    )
    yield (
        AttributeSpecification('id', 1, Operator.LT),
        [],
    )
    yield (
        AttributeSpecification('id', 3, Operator.LT),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
        ],
    )
    yield (
        AttributeSpecification('id', 3, Operator.LTE),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=3, title='Title 3', text='Text 3'),
        ],
    )
    yield (
        AndSpecification(
            AttributeSpecification('id', 5, Operator.LTE),
            AttributeSpecification('id', [2, 4], Operator.NOT_IN),
        ),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=3, title='Title 3', text='Text 3'),
            News(id=5, title='Title 5', text='Text 5'),
        ],
    )
    yield (
        AndSpecification(
            AttributeSpecification('id', 99, Operator.GTE),
            AttributeSpecification('text', None, Operator.NE),
        ),
        [
            News(id=99, title='Title 99', text='Text 99'),
            News(id=100, title='Title 100', text='Text 100'),
        ],
    )
    yield (
        AttributeSpecification('id', [1, 2, 5], Operator.IN),
        [
            News(id=1, title='Title 1', text='Text 1'),
            News(id=2, title='Title 2', text='Text 2'),
            News(id=5, title='Title 5', text='Text 5'),
        ],
    )
    yield (
        AndSpecification(
            AttributeSpecification('id', 3, Operator.GT),
            AttributeSpecification('id', 6, Operator.LT),
        ),
        [
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title 5', text='Text 5'),
        ],
    )
    yield (
        AndSpecification(
            AttributeSpecification('id', 3, Operator.GTE),
            AttributeSpecification('id', 6, Operator.LT),
        ),
        [
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title 5', text='Text 5'),
        ],
    )
    yield (
        AndSpecification(
            AttributeSpecification('id', 3, Operator.GTE),
            AttributeSpecification('id', 6, Operator.LT),
            AttributeSpecification('text', 'Text 4', Operator.NE),
        ),
        [
            News(id=3, title='Title 3', text='Text 3'),
            News(id=5, title='Title 5', text='Text 5'),
        ],
    )
    yield (
        AndSpecification(
            AttributeSpecification('id', 3, Operator.GTE),
            AttributeSpecification('id', 6, Operator.LT),
            NotSpecification(AttributeSpecification('text', 'Text 4', Operator.E)),
        ),
        [
            News(id=3, title='Title 3', text='Text 3'),
            News(id=5, title='Title 5', text='Text 5'),
        ],
    )
    yield (
        OrSpecification(
            AndSpecification(
                AttributeSpecification('id', 3, Operator.GTE),
                AttributeSpecification('id', 6, Operator.LT),
            ),
            AndSpecification(
                AttributeSpecification('id', 7, Operator.GTE),
                AttributeSpecification('id', 9, Operator.LTE),
            ),
        ),
        [
            News(id=3, title='Title 3', text='Text 3'),
            News(id=4, title='Title 4', text='Text 4'),
            News(id=5, title='Title 5', text='Text 5'),
            News(id=7, title='Title 7', text='Text 7'),
            News(id=8, title='Title 8', text='Text 8'),
            News(id=9, title='Title 9', text='Text 9'),
        ]
    )

