from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy import select, text

from database import Base, engine, SessionLocal
from models import UserTable
from schemas import UserRequest, UserCreate
from typing import List
from sqlalchemy.orm import Session
import hashlib
import bcrypt

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI(title="Users")


# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# hash password
def get_hashed_pass(passwd: str):
    salt = bcrypt.gensalt()
    hashed_pass = hashlib.md5((passwd + str(salt)).encode())
    pass_to_str = hashed_pass.hexdigest()

    return pass_to_str


# helping func
# def get_by_name(name: str):
#     query = users.select().where(users.c.email==email)
#     user = await self.database.fetch_one(query)
#     if user is None:
#         return None
#     return User.parse_obj(user)


@app.get("/")
def root():
    return "FAlearning"


@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # checking for no duplicate username // doesn't work yet(
    # user_name = session.query(UserTable.name).distinct(text('user.name'))

    user_name = select(UserTable.name).where(UserTable.name == user.name)

    print(user_name)
    print(type(user_name))

    usrdb = None
    with engine.connect() as conn:
        for row in conn.execute(user_name).first():
            print(row)
            if not row:

                # create an instance of the User db model
                usrdb = UserTable(name=row, password=get_hashed_pass(user.password))

                # add it to the session and commit it
                session.add(usrdb)
                session.commit()
                session.refresh(usrdb)
            else:
                raise HTTPException(status_code=403,
                                    detail=f"user with name {user.name} already registered")

    # return the id
    return usrdb


@app.get("/user/{id}", response_model=UserRequest)
def read_user(id: int, session: Session = Depends(get_session)):
    # get the user item with the given id
    user = session.query(UserTable).get(id)

    print(user)
    # check if UserTable item with given id exists.
    # If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(status_code=404, detail=f"user item with {id} not found")

    return user


@app.put("/user/{id}")
def update_user(id: int, name: str, password: str, session: Session = Depends(get_session)):
    # get the user item with the given id
    user = session.query(UserTable).get(id)

    # update user item the given name
    # (if an item with the given id was found)
    if user:
        user.name = name
        user.password = get_hashed_pass(password)
        session.commit()

    # check if user item with given id exists.
    # If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(status_code=404, detail=f"user item with id {id} not found")

    return user


@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Session = Depends(get_session)):
    # get the user item with the given id
    user = session.query(UserTable).get(id)

    # if user item with given id exists, delete it from the db.
    # Otherwise, raise 404 error
    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"user item with id {id} not found")

    return None


@app.get("/user", response_model=List[UserRequest])
def read_user_list(session: Session = Depends(get_session)):
    # get all user items
    user_list = session.query(UserTable).all()

    return user_list
