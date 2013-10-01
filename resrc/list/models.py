# -*- coding: utf-8 -*-:
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.core.cache import cache
from django.db import models
from django.db.models import Count
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager

from resrc.utils.templatetags.emarkdown import listmarkdown

class ListManager(models.Manager):

    def personal_lists(self, owner):
        return self.get_query_set().prefetch_related('links') \
            .filter(owner=owner) \
            .exclude(title__in=['Bookmarks', 'Reading list'])

    def user_lists(self, owner, only_public=True):
        qs = self.get_query_set().prefetch_related('links') \
            .filter(owner=owner)
        if only_public:
            qs = qs.exclude(is_public=False)
        return qs

    def all_my_list_titles(self, owner, link_pk):
        '''returns list of titles of Lists containing this Link'''
        titles = self.get_query_set().prefetch_related('links') \
            .filter(owner=owner, links__pk=link_pk)
        return titles

    def my_list_titles(self, owner, link_pk):
        '''returns  titles of my own Lists containing this Link'''
        titles = self.all_my_list_titles(owner, link_pk) \
            .exclude(title__in=['Bookmarks', 'Reading list'])
        return titles

    def some_lists_from_link(self, link_pk):
        '''To display : "as seen in..."'''
        lists = self.get_query_set().prefetch_related('links') \
            .filter(links__pk=link_pk) \
            .exclude(title__in=['Bookmarks', 'Reading list']) \
            .exclude(is_public=False)[:5]
        ''' Now excluding all private lists. To keep showing MY private
            lists : from django.db.models import Q
            .exclude(is_public=False, ~Q(owner=request.user)))
            '''
        return list(lists)

    def latest(self,limit=10):
        return self.get_query_set() \
            .exclude(title__in=['Bookmarks', 'Reading list']) \
            .exclude(is_public=False) \
            .order_by('-pubdate')[:limit]

    def most_viewed(self,limit=10):
        return self.get_query_set() \
            .exclude(title__in=['Bookmarks', 'Reading list']) \
            .exclude(is_public=False) \
            .order_by('-views')[:limit]


class List(models.Model):

    class Meta:
        verbose_name = 'List'
        verbose_name_plural = 'Lists'

    objects = ListManager()

    title = models.CharField('title', max_length=80)
    slug = models.SlugField(max_length=255)
    tags = TaggableManager()
    description = models.TextField('description')
    md_content = models.TextField('md_content')
    html_content = models.TextField('html_content')
    url = models.URLField('url', null=True, blank=True)

    links = models.ManyToManyField("link.Link", through='ListLinks')

    owner = models.ForeignKey(User, related_name="list_owner")
    is_public = models.BooleanField(default=True)
    pubdate = models.DateField(auto_now_add=True)

    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        cache.delete('list_%s' % self.pk)
        self.do_unique_slug()
        if not self.description:
            self.description = self.title
        cache.set('list_%s' % self.pk, self, 60*5)
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

    def get_tags(self):
        from taggit.models import Tag
        return Tag.objects.filter(link__list=self) \
            .values_list('name', 'slug') \
            .annotate(c=Count('name')).order_by('-c')

    def vote(self, user):
        from resrc.vote.models import Vote
        vote = Vote.objects.create(
            user=user,
            link=None,
            alist=self
        )
        vote.save()


# https://docs.djangoproject.com/en/dev/topics/db/models/#intermediary-manytomany
class ListLinks(models.Model):
    alist = models.ForeignKey('list.List')
    links = models.ForeignKey('link.Link')
    adddate = models.DateField(auto_now_add=True)

    def add(self):
        listlink = self
        alist = listlink.alist
        link = listlink.links
        md_link = "1. [%s](%s)" % (
            link.get_absolute_url(), link.title, link.url
        )
        alist.md_content = "\n".join([alist.md_content, md_link])
        alist.html_content = listmarkdown(alist.md_content, alist)
        alist.save()

    def remove(self):
        pass
        # Probably the best way is to create a listmarkdown() like to properly remove links
        # listlink = self
        # alist = listlink.alist
        # link = listlink.links
        # md_link = "[%s](%s)" % (
        #     link.get_absolute_url(), link.title, link.url
        # )

        # alist.md_content = alist.md_content.replace(md_link, '')

        # import re
        # SEARCH = re.compile("^(\d+\.|-)(\s)$", re.MULTILINE)
        # REPLACE = r' '
        # alist.md_content = SEARCH.sub(REPLACE, alist.md_content)

        # from resrc.utils.templatetags.emarkdown import listmarkdown
        # alist.html_content = listmarkdown(alist.md_content, alist)
        # alist.save()
