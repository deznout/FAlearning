import random
import string
import time

from fastapi import FastAPI, status, HTTPException, Depends

import services
from database import Base, engine, SessionLocal
from models import UserTable
from schemas import UserRequest, UserCreate
from typing import List
from sqlalchemy.orm import Session
import hashlib
import bcrypt
import logging


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI(title="Users")


@app.middleware("http")
async def log_requests(request: UserRequest, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# hash password
def get_hashed_pass(passwd):
    salt = bcrypt.gensalt()
    hashed_pass = hashlib.md5((str(passwd) + str(salt)).encode())
    pass_to_str = hashed_pass.hexdigest()

    return pass_to_str


@app.get("/")
def root():
    logger.info("logging from the root logger")
    services.echo("start root")
    return {"status": "alive"}


@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    logger.info("logging from the root logger")
    services.echo("create user process")
    # checking for no duplicate username
    user_name = session.query(UserTable.name).filter_by(name=user.name).first()

    if not user_name:

        # create an instance of the User db model
        usrdb = UserTable(name=user.name, password=get_hashed_pass(user.password))

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
    logger.info("logging from the root logger")
    services.echo("reading user")
    # get the user item with the given id
    user = session.query(UserTable).get(id)

    # check if UserTable item with given id exists.
    # If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(status_code=404, detail=f"user item with {id} not found")

    return user


@app.put("/user/{id}")
def update_user(id: int, name: str, password: str, session: Session = Depends(get_session)):
    logger.info("logging from the root logger")
    services.echo("updating")
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
    logger.info("logging from the root logger")
    services.echo("deleting user")
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
    logger.info("logging from the root logger")
    services.echo("reading all users")
    # get all user items
    user_list = session.query(UserTable).all()

    return user_list
