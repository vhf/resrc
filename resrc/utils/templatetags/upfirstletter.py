# -*- coding: utf-8 -*-:
from django import template

register = template.Library()


@register.filter()
def upfirstletter(value):
    first = value[1] if len(value) > 1 else ''
    remaining = value[2:] if len(value) > 2 else ''
    return first.upper() + remaining
