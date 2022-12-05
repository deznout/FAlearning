from sqlalchemy import Column, Integer, String
from database import Base


# Define UserTable class inheriting from Base
class UserTable(Base):
    __tablename__ = 'users_table'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    # password = Column(String(10))
