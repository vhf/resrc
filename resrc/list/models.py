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

    def user_lists(self, owner):
        return self.get_query_set().prefetch_related('links') \
            .filter(owner=owner) \
            .exclude(title__in=['Bookmarks', 'Reading list']) \
            .exclude(is_public=False)

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

    def hottest(self,limit=10):
        return self.get_query_set().order_by('score_h24')[:limit]



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
    # from resrc.utils.templatetags.emarkdown import listmarkdown
    # alist.html_content = listmarkdown(alist.md_content, alist)
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

    # from resrc.utils.templatetags.emarkdown import listmarkdown
    # alist.html_content = listmarkdown(alist.md_content)
    alist.save()
    return True
