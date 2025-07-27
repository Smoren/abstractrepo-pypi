from typing import Generator

from tests.fixtures.classes import NewsRepositoryInterface, ListBasedNewsRepository, NewsCreateForm, News


def data_provider_for_news_repo(size: int, with_no_text_item: bool = False) -> Generator[NewsRepositoryInterface, None, None]:
    repo = ListBasedNewsRepository()
    for i in range(size - int(with_no_text_item)):
        repo.create(NewsCreateForm(title=f'Title {i+1}', text=f'Text {i+1}'))

    if with_no_text_item:
        repo.create(NewsCreateForm(title=f'Title for None text', text=None))

    yield repo
