# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from resrc.link.models import Link
from resrc.tag.models import Tag


class List(models.Model):

    class Meta:
        verbose_name = 'List'
        verbose_name_plural = 'Lists'

    title = models.CharField('title', max_length=80)

    links = models.ManyToManyField(Link, related_name="%(app_label)s_%(class)s_related")

    owner = models.ForeignKey(User, related_name="list_owner")

    is_public = models.BooleanField(default=True)
