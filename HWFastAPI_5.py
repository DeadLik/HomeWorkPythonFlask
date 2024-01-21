import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from random import randint, choice

app = FastAPI()
templates = Jinja2Templates(directory='templates')
tasks = []


class Tasks(BaseModel):
    id: int
    title: str
    description: str
    at_work: bool


for i in range(1, 21):
    new_task = Tasks(id=i,
                     title=f'Title{randint(1, 50)}',
                     description=f'Description{randint(1, 50)}',
                     at_work=choice([True, False])
                     )
    tasks.append(new_task)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    table = pd.DataFrame([vars(task) for task in tasks]).to_html()
    return templates.TemplateResponse('index.html', {'request': request, 'table': table})


@app.get('/tasks/{task_id}', response_class=HTMLResponse)
async def get_task(request: Request, task_id: int):
    for task in tasks:
        if task.id == task_id:
            table = pd.DataFrame([vars(task)]).to_html()
            return templates.TemplateResponse('index.html', {'request': request, 'table': table})


@app.post('/tasks/', response_model=Tasks)
async def create_task(task: Tasks):
    tasks.append(task)
    return tasks


@app.put('/tasks/{task_id}', response_model=Tasks)
async def put_user(task_id: int, task: Tasks):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == task_id:
            task.id = task_id
            tasks[i] = task
            return task
    return tasks


@app.delete('/delete/{task_id}', response_class=HTMLResponse)
async def delete_user(task_id: int):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == task_id:
            return pd.DataFrame([vars(tasks.pop(i))]).to_html()
