# -*- coding: utf-8 -*-:
from django.db import models

from django.core import urlresolvers
from django.template.defaultfilters import slugify
from django.contrib.comments import get_model
from django.contrib.auth.models import User

from resrc.tag.models import Tag


class Link(models.Model):

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    title = models.CharField('title', max_length=120)

    url = models.URLField('url')

    pubdate = models.DateTimeField('date added', auto_now_add=True)

    author = models.ForeignKey(User, verbose_name='author')

    # upvotes = models.IntegerField('upvotes', null=True, blank=True)
    # downvotes = models.IntegerField('downvotes', null=True, blank=True)

    tags = models.ManyToManyField(
        Tag, related_name="%(app_label)s_%(class)s_related")

    def __unicode__(self):
        return self.title

    def get_slug(self):
        return slugify(self.title)

    def get_comment_count(self):
        return get_model().objects.filter(object_pk=self.pk).count()

    def get_absolute_url(self):
        return urlresolvers.reverse("link-single-slug", args=(
            self.pk,
            self.get_slug()
        ))
