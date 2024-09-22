from pydantic import BaseModel
from typing import List, Optional


class BookBase(BaseModel):
    title: str
    description: str
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookInDB(BookBase):
    id: int


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorInDB(AuthorBase):
    id: int

# Define Pydantic model for user registration
class RegisterModel(BaseModel):
    username: str
    password: str
    email: Optional[str] = None