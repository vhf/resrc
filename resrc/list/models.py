# -*- coding: utf-8 -*-:
from django.db import models
from django.contrib.auth.models import User

from resrc.link.models import Link


class ListManager(models.Manager):

    def personal_lists(self, owner):
        return self.get_query_set().prefetch_related('links') \
            .filter(owner=owner) \
            .exclude(title__in=['Bookmarks', 'Reading list'])

    def titles_link_in_default(self, owner, link_pk):
        '''returns list containing titles of default lists containing this link'''
        titles = self.get_query_set().prefetch_related('links') \
            .filter(owner=owner, links__pk=link_pk) \
            .exclude(title__in=['Bookmarks', 'Reading list']) \
            .values_list('title', flat=True)
        return list(titles)


class List(models.Model):

    class Meta:
        verbose_name = 'List'
        verbose_name_plural = 'Lists'

    objects = ListManager()

    title = models.CharField('title', max_length=80)

    description = models.TextField('description')

    links = models.ManyToManyField(Link)

    owner = models.ForeignKey(User, related_name="list_owner")

    is_public = models.BooleanField(default=True)

    is_ordered = models.BooleanField(default=False)

    pubdate = models.DateField(auto_now_add=True)
