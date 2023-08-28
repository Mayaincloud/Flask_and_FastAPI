import databases
import sqlalchemy

DATABASE_URL = "sqlite:///order.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('first_name', sqlalchemy.String(64)),
                         sqlalchemy.Column('last_name', sqlalchemy.String(64)),
                         sqlalchemy.Column('email', sqlalchemy.String(128)),
                         sqlalchemy.Column('password', sqlalchemy.String(32)),
                         )

items = sqlalchemy.Table('items',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('title', sqlalchemy.String(64)),
                         sqlalchemy.Column('description', sqlalchemy.String(128)),
                         sqlalchemy.Column('price', sqlalchemy.Float),
                         )

orders = sqlalchemy.Table('orders',
                          metadata,
                          sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                            nullable=False),
                          sqlalchemy.Column('item_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('items.id'),
                                            nullable=False),
                          sqlalchemy.Column('date', sqlalchemy.Date),
                          sqlalchemy.Column('status', sqlalchemy.String(32)),
                          )

engine = sqlalchemy.create_engine(DATABASE_URL,
                                  connect_args={"check_same_thread": False})
metadata.create_all(engine)
