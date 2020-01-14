import random
from hashids import Hashids

def get_hashid(id, min_length=6, alphabet='abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789'):
    hashids = Hashids(min_length=min_length, alphabet=alphabet)
    return hashids.encode(int(id), random.randint(0, 73))
