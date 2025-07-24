from abstractrepo.exceptions import ItemNotFoundException

from tests.fixtures.classes import ExampleNewsRepository, NewsCreateForm, NewsUpdateForm


def test_first_example():
    repo = ExampleNewsRepository()
    assert len(repo.get_list()) == 0

    repo.create(NewsCreateForm('Title 1', 'Text 1'))
    assert len(repo.get_list()) == 1

    repo.create(NewsCreateForm(title='Title 2', text='Text 2'))
    assert len(repo.get_list()) == 2

    repo.create(NewsCreateForm(title='Title 3', text='Text 3'))
    assert len(repo.get_list()) == 3

    news = repo.get_item(2)
    assert news.title == 'Title 2'
    assert news.text == 'Text 2'

    repo.update(2, NewsUpdateForm(title='Title 2 updated', text='Text 2 updated'))
    news = repo.get_item(2)
    assert news.title == 'Title 2 updated'
    assert news.text == 'Text 2 updated'

    repo.delete(2)
    assert len(repo.get_list()) == 2

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
