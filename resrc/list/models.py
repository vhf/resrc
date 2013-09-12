# -*- coding: utf-8 -*-:
from django.db import models
from django.core import urlresolvers
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from taggit.managers import TaggableManager
from resrc.link.models import Link


class ListManager(models.Manager):
    # TODO dafuq did I do. What's the diff between the following and titles_link_in_default ?
    # titles_link_in_default seems to do the opposite of what its name suggests

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

    def some_lists_from_link(self, link_pk):
        lists = self.get_query_set().prefetch_related('links') \
            .filter(links__pk=link_pk) \
            .exclude(title__in=['Bookmarks', 'Reading list']) \
            .exclude(is_public=False)[:5]
        ''' Now excluding all private lists. To keep showing MY private
            lists : from django.db.models import Q
            .exclude(is_public=False, ~Q(owner=request.user)))
            '''
        return list(lists)


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
    url = models.URLField('url', null=True, blank=True)

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

    def get_tags(self):
        from taggit.models import Tag
        from django.db.models import Count
        return Tag.objects.filter(link__list=self) \
            .values_list('name') \
            .annotate(c=Count('name')).order_by('-c')


# https://docs.djangoproject.com/en/dev/topics/db/models/#intermediary-manytomany
class ListLinks(models.Model):
    alist = models.ForeignKey(List)
    links = models.ForeignKey(Link)
    adddate = models.DateField(auto_now_add=True)


@receiver(post_save, sender=ListLinks)
def list_add_handler(sender, **kwargs):
    listlink = kwargs['instance']
    alist = listlink.alist
    link = listlink.links
    md_link = "1. [link](%s) [%s](%s)" % (
        link.get_absolute_url(), link.title, link.url
    )
    alist.md_content = "\n".join([alist.md_content, md_link])
    from resrc.utils.templatetags.emarkdown import listmarkdown
    alist.html_content = listmarkdown(alist.md_content)
    alist.save()
    return True


@receiver(pre_delete, sender=ListLinks)
def list_delete_handler(sender, **kwargs):
    listlink = kwargs['instance']
    alist = listlink.alist
    link = listlink.links
    md_link = "[link](%s) [%s](%s)" % (
        link.get_absolute_url(), link.title, link.url
    )

    alist.md_content = alist.md_content.replace(md_link, '')

    import re
    SEARCH = re.compile("^(\d+\.|-)(\s)$", re.MULTILINE)
    REPLACE = r' '
    alist.md_content = SEARCH.sub(REPLACE, alist.md_content)

    from resrc.utils.templatetags.emarkdown import listmarkdown
    alist.html_content = listmarkdown(alist.md_content)
    alist.save()
    return True
