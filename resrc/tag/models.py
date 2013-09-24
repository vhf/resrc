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

    def latest_links(self, limit=10, days=1):
        from resrc.link.models import Link
        latest = list(Link.objects.latest(limit=limit))
        voted = list(self.get_query_set() \
            .filter(time__gt=datetime.now() - timedelta(days=days)) \
            .exclude(link=None) \
            .values('link__pk', 'link__slug', 'link__title') \
            .annotate(count=Count('id')) \
            .order_by('-link__pubdate')[:limit])
        voted_id = [link['link__pk'] for link in voted]

        links = []
        for link in latest:
            if link['pk'] in voted_id:
                new_link = [l for l in voted if l['link__pk'] == link['pk']]
                links += new_link
            else:
                new_link = {}
                new_link['count'] = 0
                new_link['link__pk'] = link['pk']
                new_link['link__slug'] = link['slug']
                new_link['link__title'] = link['title']
                links += [new_link]
        return links[:limit]


    def hottest_lists(self, limit=10, days=1):
        return self.get_query_set() \
            .filter(time__gt=datetime.now() - timedelta(days=days)) \
            .exclude(alist=None) \
            .exclude(alist__is_public=False) \
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
