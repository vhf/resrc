# -*- coding: utf-8 -*-:
from django.db import models

from django.core import urlresolvers
from django.template.defaultfilters import slugify
from django.contrib.comments import get_model
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


class Link(models.Model):

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    title = models.CharField('title', max_length=120)

    slug = models.SlugField()

    url = models.URLField('url')

    pubdate = models.DateTimeField('date added', auto_now_add=True)

    author = models.ForeignKey(User, verbose_name='author')

    # upvotes = models.IntegerField('upvotes', null=True, blank=True)
    # downvotes = models.IntegerField('downvotes', null=True, blank=True)

    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.do_unique_slug()
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
