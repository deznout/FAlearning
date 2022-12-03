from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a sqlite engine instance
engine = create_engine("sqlite:///users.db")

# Create a DeclarativeMeta instance
Base = declarative_base()


# Define UserTable class inheriting from Base
class UserTable(Base):
    __tablename__ = 'users_table'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    password = Column(String(10))
