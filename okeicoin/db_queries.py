import hashlib
import random

from models import User

def registration(user_id, user_name, user_group):
    try:
        pay_account = hashlib.sha1((str(user_id) + ':' + str(user_name) + ':' + str(user_group) + ':' + str(random.randint(0, 999999))).encode('utf-8')).hexdigest()
        User.create(user_id=user_id, user_name=user_name, user_group=user_group, pay_account=pay_account, user_balance=0)
    except Exception as e:
        return 'error'
    return 'success'

def check_auth(user_id):
    try:
        user = User.get(User.user_id == user_id)
    except:
        return None
    return user.user_id

def get_info(user_id):
    user = User.get(User.user_id == user_id)

    return [user.user_name, user.user_group, user.pay_account, user.user_balance]

def get_balance(user_id):
   user = User.get(User.user_id == user_id)

   return user.user_balance

def plus_balance(user_id, count):
    user = User.get(User.user_id == user_id)
    
    user_balance = user.user_balance
    user_balance += count

    user.user_balance = user_balance
    user.save()

def check_pay_account(pay_account):
    try:
        user = User.get(User.pay_account == pay_account)
    except:
        return None
    return user.user_id

