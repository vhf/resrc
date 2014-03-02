import random

def random_digit_challenge():
    ret = u''
    for i in range(6):
        ret += str(random.randint(2,9))
    return ret, ret
