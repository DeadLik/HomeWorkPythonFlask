from fastapi import APIRouter, Request
from db import goods, database
from models.goods import Goods, GoodsIn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post("/goods", response_model=Goods)
async def create_goods(new_goods: GoodsIn):
    query = goods.insert().values(**new_goods.model_dump())
    last_record_id = await database.execute(query)
    return {**new_goods.model_dump(), "id": last_record_id}


@router.put("/goods/{goods_id}")
async def update_goods(goods_id: int, new_goods: GoodsIn):
    query = goods.update().where(goods.c.id == goods_id).values(**new_goods.model_dump())
    await database.execute(query)
    return {**new_goods.model_dump(), "id": goods_id}


@router.get("/all_goods/", response_class=HTMLResponse)
async def read_all_goods(request: Request):
    query = goods.select()
    goods_table = pd.DataFrame([product for product in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse('goods.html', {'request': request, 'goods_table': goods_table})


@router.get("/goods/{goods_id}", response_model=Goods)
async def read_goods(goods_id: int):
    query = goods.select().where(goods.c.id == goods_id)
    return await database.fetch_one(query)


@router.delete("/goods/{goods_id}")
async def delete_goods(goods_id: int):
    query = goods.delete().where(goods.c.id == goods_id)
    await database.execute(query)
    return {'message': 'Goods deleted'}
