import datetime
import random
from fastapi import APIRouter, Request
from db import goods, database, orders, users
from models.order import Order, OrderIn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post("/order/{user_id}/{goods_id}", response_model=OrderIn)
async def create_order(user_id: int, goods_id: int, new_order: OrderIn):
    query = orders.insert().values(user_id=user_id, goods_id=goods_id,
                                   order_date=datetime.datetime.now().strftime("%d/%m/%y, %H:%M:%S"),
                                   status=new_order.status)
    last_record_id = await database.execute(query)
    return {**new_order.model_dump(), "id": last_record_id}


@router.put("/order/{order_id}", response_model=OrderIn)
async def update_order(order_id, new_goods: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(status=new_goods.status,
                                                                  order_date=datetime.datetime.now().strftime(
                                                                      "%d/%m/%y, %H:%M:%S"))
    await database.execute(query)
    return {**new_goods.model_dump(), "id": order_id}


@router.get("/orders/", response_class=HTMLResponse)
async def read_orders(request: Request):
    query = orders.select()
    order_table = pd.DataFrame([order for order in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse('orders.html', {'request': request, 'order_table': order_table})


@router.get("/order/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@router.delete("/order/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)

    await database.execute(query)
    return {'message': 'Goods deleted'}
