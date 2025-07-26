from abstractrepo.exceptions import ItemNotFoundException
from abstractrepo.specification import Operator, AttributeSpecification, AndSpecification, OrSpecification
from abstractrepo.order import OrderDirection, OrderOptionsBuilder
from abstractrepo.paging import PagingOptions, Paginator

from tests.fixtures.classes import ListBasedNewsRepository, NewsCreateForm, NewsUpdateForm


def test_first_example():
    repo = ListBasedNewsRepository()
    assert len(repo.get_collection()) == 0

    model = repo.create(NewsCreateForm(title='Title 1', text='Text 1'))
    assert len(repo.get_collection()) == 1
    assert repo.exists(model.id)

    model = repo.create(NewsCreateForm(title='Title 2', text='Text 2'))
    assert len(repo.get_collection()) == 2
    assert repo.exists(model.id)

    model = repo.create(NewsCreateForm(title='Title 3', text='Text 3'))
    assert len(repo.get_collection()) == 3
    assert repo.exists(model.id)

    news = repo.get_item(2)
    assert news.title == 'Title 2'
    assert news.text == 'Text 2'

    repo.update(2, NewsUpdateForm(title='Title 2 updated', text='Text 2 updated'))
    news = repo.get_item(2)
    assert news.title == 'Title 2 updated'
    assert news.text == 'Text 2 updated'

    repo.delete(2)
    assert len(repo.get_collection()) == 2

    try:
        repo.get_item(2)
        assert False
    except ItemNotFoundException:
        assert True

    try:
        repo.update(2, NewsUpdateForm(title='Title 2', text='Text 2'))
        assert False
    except ItemNotFoundException:
        assert True

    try:
        repo.delete(2)
        assert False
    except ItemNotFoundException:
        assert True


def test_get_list_example():
    repo = ListBasedNewsRepository()
    assert len(repo.get_collection()) == 0

    repo.create(NewsCreateForm(title='First Topic 1', text='First topic text 1'))
    repo.create(NewsCreateForm(title='First Topic 2', text='First topic text 2'))
    repo.create(NewsCreateForm(title='First Topic 3', text='First topix text 3'))
    repo.create(NewsCreateForm(title='Second Topic 1', text='Second topic text 1'))
    repo.create(NewsCreateForm(title='Second Topic 2', text='Second topic text 2'))
    repo.create(NewsCreateForm(title='Second Topic 3', text='Second topic text 3'))
    repo.create(NewsCreateForm(title='Third Theme 1', text='Third topic text 1'))
    repo.create(NewsCreateForm(title='Third Theme 2', text='Third topic text 2'))
    repo.create(NewsCreateForm(title='Third Theme 3', text='Third topic text 3'))
    assert len(repo.get_collection()) == 9

    filter_spec = AttributeSpecification('title', 'First Topic%', Operator.ILIKE)
    news_list = repo.get_collection(filter_spec=filter_spec)
    assert len(news_list) == 3
    assert [news.title for news in news_list] == ['First Topic 1', 'First Topic 2', 'First Topic 3']

    filter_spec = AndSpecification(
        AttributeSpecification('title', '%Topic%', Operator.ILIKE),
        AttributeSpecification('text', '%1', Operator.ILIKE)
    )
    news_list = repo.get_collection(filter_spec=filter_spec)
    assert len(news_list) == 2
    assert [news.title for news in news_list] == ['First Topic 1', 'Second Topic 1']

    filter_spec = AttributeSpecification('title', '%Topic%', Operator.ILIKE)
    first_page = PagingOptions(3, 0)
    news_list = repo.get_collection(filter_spec=filter_spec, paging_options=first_page)
    assert len(news_list) == 3
    assert [news.title for news in news_list] == ['First Topic 1', 'First Topic 2', 'First Topic 3']

    second_page = PagingOptions(3, 3)
    news_list = repo.get_collection(filter_spec=filter_spec, paging_options=second_page)
    assert len(news_list) == 3
    assert [news.title for news in news_list] == ['Second Topic 1', 'Second Topic 2', 'Second Topic 3']

    paginator = Paginator(page_size=3, start_page=1)
    first_page = paginator.get_page(1)
    news_list = repo.get_collection(filter_spec=filter_spec, paging_options=first_page)
    assert len(news_list) == 3
    assert [news.title for news in news_list] == ['First Topic 1', 'First Topic 2', 'First Topic 3']

    second_page = paginator.get_page(2)
    news_list = repo.get_collection(filter_spec=filter_spec, paging_options=second_page)
    assert len(news_list) == 3
    assert [news.title for news in news_list] == ['Second Topic 1', 'Second Topic 2', 'Second Topic 3']

    order_by_id_desc = OrderOptionsBuilder().add('id', OrderDirection.DESC).build()
    first_page = PagingOptions(3, 0)
    news_list = repo.get_collection(filter_spec=filter_spec, order_options=order_by_id_desc, paging_options=first_page)
    assert len(news_list) == 3
    assert [news.title for news in news_list] == ['Second Topic 3', 'Second Topic 2', 'Second Topic 1']

    second_page = PagingOptions(3, 3)
    news_list = repo.get_collection(filter_spec=filter_spec, order_options=order_by_id_desc, paging_options=second_page)
    assert len(news_list) == 3
    assert [news.title for news in news_list] == ['First Topic 3', 'First Topic 2', 'First Topic 1']

    filter_spec = OrSpecification(
        AttributeSpecification('title', '%Topic%', Operator.ILIKE),
        AttributeSpecification('text', 'Third topic text 1', Operator.E)
    )
    news_list = repo.get_collection(filter_spec=filter_spec)
    assert len(news_list) == 7
    assert [news.title for news in news_list] == ['First Topic 1', 'First Topic 2', 'First Topic 3', 'Second Topic 1', 'Second Topic 2', 'Second Topic 3', 'Third Theme 1']

    filter_spec = AttributeSpecification('id', [1, 2], Operator.IN)
    news_list = repo.get_collection(filter_spec=filter_spec)
    assert len(news_list) == 2
    assert [news.id for news in news_list] == [1, 2]
