from pydantic import BaseModel

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
