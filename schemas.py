from pydantic import BaseModel


# Create UserRequest Schema (Pydantic Model)
class UserRequestCreate(BaseModel):
    name: str
    # password: str


# Complete UserRequest Schema (Pydantic Model)
class UserRequest(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
