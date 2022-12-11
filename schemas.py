from pydantic import BaseModel, SecretStr


# Create UserRequest Schema (Pydantic Model)
class UserCreate(BaseModel):
    name: str
    password: SecretStr


# Complete UserRequest Schema (Pydantic Model)
class UserRequest(BaseModel):
    id: int
    name: str
    password: SecretStr

    class Config:
        orm_mode = True
