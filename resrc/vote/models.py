# -*- coding: utf-8 -*-:
from django.db import models
from django.db.models import Count
from django.utils.timezone import utc
from datetime import timedelta, datetime
from django.contrib.auth.models import User

from mptt_comments.models import MpttComment


class VoteManager(models.Manager):

    def my_upvoted_links(self, user):
        qs = self.get_query_set() \
            .filter(user=user)
        qs = qs \
            .exclude(link=None) \
            .values('link__pk', 'link__slug', 'link__title') \
            .annotate(count=Count('id')) \
            .order_by('-time')
        return qs


    def my_upvoted_lists(self, user):
        return self.get_query_set() \
            .exclude(alist=None) \
            .filter(user=user) \
            .values('alist__pk', 'alist__slug', 'alist__title') \
            .annotate(count=Count('id')) \
            .order_by('-time')


    def hottest_links(self, limit=10, days=1, lang_filter=[1]):
        qs = self.get_query_set() \
            .filter(time__gt=datetime.utcnow().replace(tzinfo=utc) - timedelta(days=days))
        if lang_filter:
            qs = qs.filter(link__language__in=lang_filter)
        qs = qs \
            .exclude(link=None) \
            .values('link__pk', 'link__slug', 'link__title') \
            .annotate(count=Count('id')) \
            .order_by('-count')[:limit]

        for link in qs:
            link['commentcount'] = MpttComment.objects.filter(object_pk=link['link__pk']).count()
        return qs


    def latest_links(self, limit=10, days=1, lang_filter=[1]):
        from resrc.link.models import Link
        latest = list(Link.objects.latest(limit=limit))
        voted = self.get_query_set() \
            .filter(time__gt=datetime.utcnow().replace(tzinfo=utc) - timedelta(days=days)) \
            .exclude(link=None)
        if lang_filter:
            voted = voted.filter(link__language__in=lang_filter)

        voted = voted \
            .values('link__pk', 'link__slug', 'link__title') \
            .annotate(count=Count('id')) \
            .order_by('-link__pubdate')[:limit]
        voted = list(voted)

        voted_id = [link['link__pk'] for link in voted]

        links = []
        for link in latest:
            comment_count = MpttComment.objects.filter(object_pk=link['pk']).count()
            if link['pk'] in voted_id:
                new_link = [l for l in voted if l['link__pk'] == link['pk']]
                for l in new_link:
                    l['commentcount'] = comment_count
                links += new_link
            else:
                new_link = {}
                new_link['count'] = 0
                new_link['link__pk'] = link['pk']
                new_link['link__slug'] = link['slug']
                new_link['link__title'] = link['title']
                new_link['commentcount'] = comment_count 
                links += [new_link]
        return links[:limit]


    def hottest_lists(self, limit=10, days=1, lang_filter=[1]):  # TODO: implement lang filter
        return self.get_query_set() \
            .filter(time__gt=datetime.utcnow().replace(tzinfo=utc) - timedelta(days=days)) \
            .exclude(alist=None) \
            .exclude(alist__is_public=False) \
            .values('alist__pk', 'alist__slug', 'alist__title') \
            .annotate(count=Count('id')) \
            .order_by('-count')[:limit]


    def votes_for_link(self, link_pk):
        return len(list(self.get_query_set() \
            .filter(link__pk=link_pk)))


    def votes_for_list(self, list_pk):
        return len(list(self.get_query_set() \
            .filter(alist__pk=list_pk)))


class Vote(models.Model):

    objects = VoteManager()

    user = models.ForeignKey(User, verbose_name='user')
    alist = models.ForeignKey('list.List', null=True, blank=True)
    link = models.ForeignKey('link.Link', null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
