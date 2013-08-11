# -*- coding: utf-8 -*-:
from hashlib import md5
from time import time


def generate_token():
    return md5('Oh ah ohohoho. {0} hey haha'.format(time())).hexdigest()[:12]


def get_token(request):
    return {'get_token': request.session.get('get_token')}
