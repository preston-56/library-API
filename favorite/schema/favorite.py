from pydantic import BaseModel

class FavoriteBase(BaseModel):
    user_id: int
    book_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteInDB(FavoriteBase):
    id: int
