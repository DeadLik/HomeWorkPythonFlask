from fastapi import FastAPI
from db import database
from routers import user, goods, order

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(user.router, tags=["users"])
app.include_router(goods.router, tags=["goods"])
app.include_router(order.router, tags=["order"])
