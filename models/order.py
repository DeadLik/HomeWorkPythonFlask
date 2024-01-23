from pydantic import BaseModel, Field


class Order(BaseModel):
    id: int
    user_id: int
    goods_id: int
    order_date: str


class OrderIn(BaseModel):
    status: str
