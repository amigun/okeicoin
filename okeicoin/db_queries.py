import hashlib
import random
import string

from models import User
from models import AccessToGetOkeicoins as Atgo

def registration(user_id, user_name, user_group):
    try:
        pay_account = hashlib.sha1((str(user_id) + ':' + str(user_name) + ':' + str(user_group) + ':' + str(random.randint(0, 999999))).encode('utf-8')).hexdigest()
        User.create(user_id=user_id, user_name=user_name, user_group=user_group, pay_account=pay_account, user_balance=0, user_status=0)
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

def to_become_admin(user_id):
    user = User.get(User.user_id == user_id)

    user.user_status = 1

    user.save()

def check_status(user_id):
    user = User.get(User.user_id == user_id)

    roles = ['student', 'admin']

    return roles[int(user.user_status)]

def create_qr(count_of):
    def gen_random_string():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    qr_hash_first = gen_random_string()
    qr_hash_second = gen_random_string()

    Atgo.create(count_of=count_of, qr_hash_first=qr_hash_first, qr_hash_second=qr_hash_second, used=0)

    return qr_hash_first + ':' + qr_hash_second

def qrc_coins(returned):
    returned = returned.split(':')
    
    atgo = Atgo.get(Atgo.qr_hash_first == returned[0] and Atgo.qr_hash_second == returned[1])

    if atgo.used == 1:
        return 'used'
    else:
        atgo.used = 1
        atgo.save()

        return atgo.count_of
