# -*- coding: utf-8 -*-:
from django.db import models
from django.contrib.auth.models import User

from resrc.link.models import Link
from resrc.tag.models import Tag


class List(models.Model):

    class Meta:
        verbose_name = 'List'
        verbose_name_plural = 'Lists'

    title = models.CharField('title', max_length=80)

    description = models.TextField('description')

    links = models.ManyToManyField(
        Link,
        through='ListLinks',
        related_name="%(app_label)s_%(class)s_related")

    owner = models.ForeignKey(User, related_name="list_owner")

    is_public = models.BooleanField(default=True)

    is_ordered = models.BooleanField(default=False)

    pubdate = models.DateField(auto_now_add=True)


# https://docs.djangoproject.com/en/dev/topics/db/models/#intermediary-manytomany
class ListLinks(models.Model):
    alist = models.ForeignKey(List)
    links = models.ForeignKey(Link)
    position_in_list = models.IntegerField(blank=True)
