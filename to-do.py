from fastapi import Depends, FastAPI, HTTPException, Query
from model import Todos
from typing import Annotated, List
from sqlmodel import Field, Session, SQLModel, create_engine, select


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

apper = FastAPI()

@apper.on_event("startup")
def on_startup():
    create_db_and_tables()

#create a todo
@apper.post("/todos/")
def create_todo(todo: Todos, session: SessionDep) -> Todos:
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

#get todos
@apper.get("/todos/")
def get_todos(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Todos]:
    todos = session.exec(select(Todos).offset(offset).limit(limit)).all()
    return todos

#get a todo
@apper.get("/todos/{todo_id}")
def get_todo(todo_id: int, session: SessionDep) -> Todos:
    todo = session.get(Todos, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Hero not found")
    return todo

#delete a todo
@apper.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: SessionDep):
    todo = session.get(Todos, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(todo)
    session.commit()
    return {"ok": True}
