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

class AccessToGetOkeicoins(Model):
    count_of = IntegerField()
    qr_hash_first = TextField()
    qr_hash_second = TextField()
    used = IntegerField()

    class Meta:
        database = db

User.create_table()
AccessToGetOkeicoins.create_table()
