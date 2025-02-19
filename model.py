from fastapi import Depends, FastAPI, HTTPException, Query
#from model import Todo
from pydantic import BaseModel
from typing import Annotated, List
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Todo(BaseModel):
    id: int
    item: str

class Todos(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item: str = Field(index=True)
    #age: int | None = Field(default=None, index=True)
    #secret_name: str

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None