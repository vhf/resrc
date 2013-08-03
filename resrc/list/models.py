# -*- coding: utf-8 -*-:
from django.db import models
from django.core import urlresolvers
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from resrc.utils.templatetags.emarkdown import emarkdown
from taggit.managers import TaggableManager
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
    slug = models.SlugField()
    tags = TaggableManager()
    description = models.TextField('description')
    md_content = models.TextField('md_content')
    html_content = models.TextField('html_content')

    links = models.ManyToManyField(Link, through='ListLinks')

    owner = models.ForeignKey(User, related_name="list_owner")
    is_public = models.BooleanField(default=True)
    pubdate = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.do_unique_slug()
        if not self.description:
            self.description = self.title
        super(List, self).save(*args, **kwargs)

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
            lists = List.objects.filter(slug=slug)
            if not lists.exists():
                return slug

            slug = '%s-%s' % (orig_slug, counter)
            counter += 1

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return urlresolvers.reverse("list-single-slug", args=(
            self.pk,
            self.slug
        ))


# FIXME: not called when adding/removing a link from the list...
@receiver(pre_save, sender=List)
def list_save_handler(sender, **kwargs):
    alist = kwargs['instance']
    alist.html_content = emarkdown(alist.md_content)
    return True


# https://docs.djangoproject.com/en/dev/topics/db/models/#intermediary-manytomany
class ListLinks(models.Model):
    alist = models.ForeignKey(List)
    links = models.ForeignKey(Link)
    adddate = models.DateField(auto_now_add=True)
