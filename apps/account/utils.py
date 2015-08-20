import hashlib
import random


def generate_key(username, email):
    key = hashlib.md5()
    key.update(username + email +  str(random.random()))
    return key.hexdigest()
