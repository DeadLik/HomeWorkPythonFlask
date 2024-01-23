from fastapi import APIRouter, Request
from db import users, database
from models.user import User, UserIn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post("/user", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@router.put("/users/{user_id}")
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@router.get("/users/", response_class=HTMLResponse)
async def read_users(request: Request):
    query = users.select()
    user_table = pd.DataFrame([user for user in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse('users.html', {'request': request, 'user_table': user_table})


@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}
