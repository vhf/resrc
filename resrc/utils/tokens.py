# -*- coding: utf-8 -*-:
from hashlib import md5
from time import time


def generate_token():
    return md5('lcdldses?nas. {0} salt'.format(time())).hexdigest()[:12]


def get_token(request):
    return {'get_token': request.session.get('get_token')}
