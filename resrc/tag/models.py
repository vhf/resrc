# -*- coding: utf-8 -*-:
from django.db import models
from django.conf import settings
from django.db.models import Count
from datetime import timedelta, datetime

class Language(models.Model):
    language = models.CharField(max_length=7, choices=settings.LANGUAGES)


class VoteManager(models.Manager):

    def hottest_links(self, limit=10, days=1):
        return self.get_query_set() \
            .filter(time__gt=datetime.now() - timedelta(days=days)) \
            .exclude(link=None) \
            .values('link__pk', 'link__slug', 'link__title') \
            .annotate(count=Count('id')) \
            .order_by('-count')[:limit]

    def hottest_lists(self, limit=10, days=1):
        return self.get_query_set() \
            .filter(time__gt=datetime.now() - timedelta(days=days)) \
            .exclude(alist=None) \
            .values('alist__pk', 'alist__slug', 'alist__title') \
            .annotate(count=Count('id')) \
            .order_by('-count')[:limit]


class Vote(models.Model):

    objects = VoteManager()

    from resrc.link.models import Link
    from resrc.list.models import List
    from django.contrib.auth.models import User
    user = models.ForeignKey(User, verbose_name='user')
    alist = models.ForeignKey(List, null=True, blank=True)
    link = models.ForeignKey(Link, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
