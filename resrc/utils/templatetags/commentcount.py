# -*- coding: utf-8 -*-:
from django import template

register = template.Library()


def commentcount(pk):
    from mptt_comments.models import MpttComment
    return MpttComment.objects.filter(object_pk=pk).count()

register.simple_tag(commentcount)
