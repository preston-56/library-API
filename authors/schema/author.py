from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorInDB(AuthorBase):
    id: int
