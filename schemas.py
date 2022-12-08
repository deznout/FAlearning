from pydantic import BaseModel, ValidationError, validator


# Create UserRequest Schema (Pydantic Model)
class UserCreate(BaseModel):
    name: str
    password: str

    # @validator('name')
    # def name_must_unique(self, v):
    #     if


# Complete UserRequest Schema (Pydantic Model)
class UserRequest(BaseModel):
    id: int
    name: str
    password: str

    class Config:
        orm_mode = True
