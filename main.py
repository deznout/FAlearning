from fastapi import FastAPI, status
from database import Base, engine, UserTable
from pydantic import BaseModel
from sqlalchemy.orm import Session


# Create UserRequest Base Model
class UserRequest(BaseModel):
    name: str
    password: str


# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


@app.get("/")
def root():
    return "FAlearning"


@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequest):
    # create a new db session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the User db model
    usrdb = UserTable(name=user.name, password=user.password)

    # add it to the session and commit it
    session.add(usrdb)
    session.commit()

    # grab the id given to the obj from the db
    id = usrdb.id

    # close the session
    session.close()

    # return the id
    return f"created user item with id {id}"


@app.get("/user/{id}")
def read_user(id: int):
    return "read user item with id {id}"


@app.put("/user/{id}")
def update_user(id: int):
    return "update user item with id {id}"


@app.delete("/user/{id}")
def delete_user(id: int):
    return "delete user item with id {id}"


@app.get("/user")
def read_user_list():
    return "read user list"
