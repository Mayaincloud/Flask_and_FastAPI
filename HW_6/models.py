import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str = Field(title='First name', min_length=3, max_length=64)
    last_name: str = Field(title='Last name', min_length=3, max_length=64)
    email: str = Field(title='Email', min_length=9, max_length=128)
    password: str = Field(title='Password', min_length=3, max_length=32)


class User(UserBase):
    id: int


class ItemBase(BaseModel):
    title: str = Field(title='Name', min_length=3, max_length=64)
    description: str = Field(title='Description', min_length=3, max_length=128)
    price: float


class Item(ItemBase):
    id: int


class OrderBase(BaseModel):
    id: int
    user_id: int = Field(title='User Id')
    item_id: int = Field(title='Item Id')
    status: str = Field(title='Status', default='Placed')
    order_date: datetime.date = Field(title='Date')


class Order(OrderBase):
    order: OrderBase
    user: User
    item: Item
