# -*- coding: utf-8 -*-:
from django.db import models

from django.core import urlresolvers
from django.template.defaultfilters import slugify
from django.contrib.comments import get_model
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


class LinkManager(models.Manager):

    def latest(self,limit=10):
        return self.get_query_set().order_by('pubdate')[:limit]

    def hottest(self,limit=10):
        return self.get_query_set().order_by('score_h24')[:limit]


class Link(models.Model):

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    objects = LinkManager()

    title = models.CharField('title', max_length=120)

    slug = models.SlugField(max_length=255)

    hash2 = models.CharField(max_length=11, editable=False)

    url = models.URLField('url')

    pubdate = models.DateTimeField(
        'date added', auto_now_add=True, editable=False)

    author = models.ForeignKey(User, verbose_name='author')

    upvotes = models.IntegerField('upvotes', default=0)
    votes_h00 = models.IntegerField(default=0)
    votes_h02 = models.IntegerField(default=0)
    votes_h04 = models.IntegerField(default=0)
    votes_h06 = models.IntegerField(default=0)
    votes_h08 = models.IntegerField(default=0)
    votes_h10 = models.IntegerField(default=0)
    votes_h12 = models.IntegerField(default=0)
    votes_h14 = models.IntegerField(default=0)
    votes_h16 = models.IntegerField(default=0)
    votes_h18 = models.IntegerField(default=0)
    votes_h20 = models.IntegerField(default=0)
    votes_h22 = models.IntegerField(default=0)

    score_h24 = models.IntegerField(default=0)

    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.do_unique_slug()
        if not self.id:
            from resrc.utils.hash2 import hash2
            self.hash2 = hash2(self.url)
        super(Link, self).save(*args, **kwargs)

    def do_unique_slug(self):
        """
        Ensures that the slug is always unique for this post
        """
        if not self.id:
            # make sure we have a slug first
            if not len(self.slug.strip()):
                self.slug = slugify(self.title)

            self.slug = self.get_unique_slug(self.slug)
            return True

        return False

    def get_unique_slug(self, slug):
        """
        Iterates until a unique slug is found
        """
        orig_slug = slug
        counter = 1

        while True:
            links = Link.objects.filter(slug=slug)
            if not links.exists():
                return slug

            slug = '%s-%s' % (orig_slug, counter)
            counter += 1

    def __unicode__(self):
        return self.title

    def get_comment_count(self):
        return get_model().objects.filter(object_pk=self.pk).count()

    def get_absolute_url(self):
        return urlresolvers.reverse("link-single-slug", args=(
            self.pk,
            self.slug
        ))

    def vote(self):
        from datetime import datetime
        hour = datetime.now().hour
        hours = {
            0: 'votes_h00', 1: 'votes_h00', 2: 'votes_h02', 3: 'votes_h02', 4: 'votes_h04',
            5: 'votes_h04', 6: 'votes_h06', 7: 'votes_h06', 8: 'votes_h08', 9: 'votes_h08',
            10: 'votes_h10', 11: 'votes_h10', 12: 'votes_h12', 13: 'votes_h12', 14: 'votes_h14',
            15: 'votes_h14', 16: 'votes_h16', 17: 'votes_h16', 18: 'votes_h18', 19: 'votes_h18',
            20: 'votes_h20', 21: 'votes_h20', 22: 'votes_h22', 23: 'votes_h22'}
        link = self
        link.upvotes = link.upvotes + 1
        attr = getattr(link, hours[hour])
        setattr(link, hours[hour], attr + 1)
        setattr(link, hours[(hour + 2) % 24], 0)

        gravity = 1.8
        item_hour_age = 2
        votes = sum([getattr(link, hours[h]) for h in xrange(0, 24, 2)])
        link.score_h24 = (votes - 1) / pow((item_hour_age + 2), gravity)
        link.save()
