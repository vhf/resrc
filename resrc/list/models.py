# -*- coding: utf-8 -*-:
from django.db import models
from django.core import urlresolvers
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from resrc.utils.templatetags.emarkdown import emarkdown
from resrc.link.models import Link


class ListManager(models.Manager):

    def personal_lists(self, owner):
        return self.get_query_set().prefetch_related('links') \
            .filter(owner=owner) \
            .exclude(title__in=['Bookmarks', 'Reading list'])

    def titles_link_in(self, owner, link_pk):
        '''returns list containing titles of Lists containing this Link'''
        titles = self.get_query_set().prefetch_related('links') \
            .filter(owner=owner, links__pk=link_pk) \
            .values_list('title', flat=True)
        return list(titles)

    def titles_link_in_default(self, owner, link_pk):
        '''returns list containing titles of default Lists containing this Link'''
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
    md_content = models.TextField('md_content')
    html_content = models.TextField('html_content')

    links = models.ManyToManyField(Link)

    owner = models.ForeignKey(User, related_name="list_owner")
    is_public = models.BooleanField(default=True)
    is_ordered = models.BooleanField(default=False)
    pubdate = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return urlresolvers.reverse("list-single-slug", args=(
            self.pk,
            self.get_slug()
        ))


# FIXME: not called when adding/removing a link from the list...
@receiver(pre_save, sender=List)
def list_save_handler(sender, **kwargs):
    alist = kwargs['instance']
    alist.html_content = emarkdown(alist.md_content)
    return True
