from pydantic import BaseModel

class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
