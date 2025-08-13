from typing import Optional, Union


class News:
    id: int
    title: str
    text: Optional[str]

    def __init__(self, id: int, title: str, text: Optional[str] = None):
        self.id = id
        self.title = title
        self.text = text


class NewsCreateForm:
    title: str
    text: Union[str, None]

    def __init__(self, title: str, text: Optional[str] = None):
        self.title = title
        self.text = text


class NewsUpdateForm:
    title: str
    text: str

    def __init__(self, title: str, text: Optional[str] = None):
        self.title = title
        self.text = text


class User:
    id: int
    username: str
    password: str
    display_name: str

    def __init__(self, id: int, username: str, password: str, display_name: str):
        self.id = id
        self.username = username
        self.password = password
        self.display_name = display_name


class UserCreateForm:
    username: str
    password: str
    display_name: str

    def __init__(self, username: str, password: str, display_name: str):
        self.username = username
        self.password = password
        self.display_name = display_name


class UserUpdateForm:
    display_name: str

    def __init__(self, display_name: str):
        self.display_name = display_name
