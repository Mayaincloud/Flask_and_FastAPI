# Задание №6
# Необходимо создать базу данных для интернет-магазина. База данных должна
# состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
# содержать информацию о доступных товарах, их описаниях и ценах. Таблица
# пользователи должна содержать информацию о зарегистрированных
# пользователях магазина. Таблица заказы должна содержать информацию о
# заказах, сделанных пользователями.
# ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
# имя, фамилия, адрес электронной почты и пароль.
# ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
# название, описание и цена.
# ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
# пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
# заказа.
# Создайте модели pydantic для получения новых данных и
# возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей).
# Реализуйте CRUD операции для каждой из таблиц через
# создание маршрутов, REST API (итого 15 маршрутов).
# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление


from d_b import *
from models import *
from fastapi import FastAPI
from fastapi import Request
from random import randint
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")

app = FastAPI()


# Создание тестовых пользователей
@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(1, count + 1):
        query = users.insert().values(
            first_name=f'user_{i}',
            last_name=f'lastname_{i}',
            password=f'123{i}',
            email=f'user_{i}@mail.ru')
        await database.execute(query)
    return {'message': f' {count} fake users create'}


# Создание тестовых продуктов
@app.get("/fake_items/{count}")
async def create_fake_items(count: int):
    for i in range(1, count + 1):
        query = items.insert().values(
            title=f'product_{i}',
            description=f'description_{i}',
            price=randint(1, 100000))
        await database.execute(query)
    return {'message': f'{count} fake items create'}


# CRUD операции для пользователей
@app.post("/create_user/", response_model=User)
async def create_user(user: UserBase):
    query = users.insert().values(
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        email=user.email)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/read_users/", response_class=HTMLResponse)
async def read_users(request: Request):
    query = users.select()
    return templates.TemplateResponse('users.html', {'request': request, 'users': await database.fetch_all(query)})


@app.get("/user_id/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/update_user/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserBase):
    query = users.update().where(users.c.id ==
                                 user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


# CRUD операции для товаров
@app.post("/items/", response_model=Item)
async def create_item(item: ItemBase):
    query = items.insert().values(
        title=item.title,
        description=item.description,
        price=item.price)
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}


@app.get("/items/", response_class=HTMLResponse)
async def read_items(request: Request):
    query = items.select()
    return templates.TemplateResponse('items.html', {'request': request, 'items': await database.fetch_all(query)})


@app.get("/item_id/{item_id}", response_model=Item)
async def read_item(product_id: int):
    query = items.select().where(items.c.id == product_id)
    return await database.fetch_one(query)


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, new_item: ItemBase):
    query = items.update().where(items.c.id == item_id).values(**new_item.dict())
    await database.execute(query)
    return {**new_item.dict(), "id": item_id}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {'message': 'Item deleted'}


# CRUD операции для заказов
@app.post('/orders/', response_model=dict)
async def create_orders(order: OrderBase):
    query = orders.insert().values(
        user_id=order.user_id,
        item_id=order.item_id,
        date=order.date,
        status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.get('/orders/', response_model=list)
async def read_orders():
    query = sqlalchemy.select([orders, items, users]).where((
        users.c.id == orders.c.user_id) & (items.c.id == orders.c.item_id))
    rows = await database.fetch_all(query)
    return [
        Order(
            order=OrderBase(id=row[0], status=row[4], date=row[3], user_id=row[1], item_id=row[2]),
            user=User(id=row[9], first_name=row[10], last_name=row[11], password=row[13], email=row[12], ),
            item=Item(id=row[5], title=row[6], description=row[7], price=row[8], ))
        for row in rows]


@app.get("/order_id/{order_id}", response_model=OrderBase)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=OrderBase)
async def update_order(order_id: int, new_order: OrderBase):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
