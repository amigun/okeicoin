from peewee import *

db = SqliteDatabase('../database.db')

class User(Model):
    user_id = IntegerField()
    user_name = TextField()
    user_group = TextField()
    pay_account = TextField()
    user_balance = IntegerField()
    user_status = IntegerField()

    class Meta:
        database = db

User.create_table()
