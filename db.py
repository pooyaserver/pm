from peewee import *

db = SqliteDatabase('Base.db')

class Base(Model):
    class Meta:
        database = db

class users(Base):
    user_id = BigIntegerField(primary_key = True)
    is_ban = CharField(default = 0)

db.connect()
db.create_tables([users])