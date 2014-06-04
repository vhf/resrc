# -*- coding: utf-8 -*-:
from django.contrib.auth.models import User
from django.contrib.comments import get_model
from django.core import urlresolvers
from django.core.cache import cache
from django.db import models
from django.shortcuts import get_object_or_404
from resrc.utils import slugify

from taggit.managers import TaggableManager


LEVELS = ['beginner', 'intermediate', 'advanced']

class LinkManager(models.Manager):

    def latest(self,limit=10, lang_filter=[1]):
        qs = self.get_query_set()
        if lang_filter:
            qs = qs.filter(language__in=lang_filter)
            qs = qs.exclude(flagged=True)
        qs = qs.values('pk', 'slug', 'title') \
               .order_by('-pubdate')[:limit]
        return qs


class Link(models.Model):

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    objects = LinkManager()

    title = models.CharField('title', max_length=120)

    content = models.TextField()

    slug = models.SlugField(max_length=255)

    url = models.URLField('url')

    pubdate = models.DateTimeField(
        'date added', auto_now_add=True, editable=False)

    author = models.ForeignKey(User, verbose_name='author')

    level = models.CharField('Level', max_length=30, choices=zip(LEVELS, LEVELS), null=True, blank=True)

    language = models.ForeignKey('language.Language', default=1)

    flagged = models.BooleanField(default=False)

    tags = TaggableManager()

    def save(self, *args, **kwargs):
        cache.delete('link_%s' % self.pk)
        self.do_unique_slug()
        if not self.id:
            from resrc.utils.karma import karma_rate
            karma_rate(self.author_id, 1)
        cache.set('link_%s' % self.pk, self, 60*5)
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

    def get_absolute_url(self):
        return urlresolvers.reverse("link-single-slug", kwargs={
            'link_pk': self.pk,
            'link_slug': self.slug
        })

    def get_lang(self):
        from django.conf import settings
        return [x[1] for x in settings.LANGUAGES if x[0] == self.language.language][0]

    def vote(self, user, list_pk=None):
        from resrc.vote.models import Vote
        # we keep track of list because if link is voted from a list, we also vote for the list
        if list_pk is not None:
            from resrc.list.models import List
            alist = get_object_or_404(List, pk=list_pk)
        else:
            alist = None
        vote = Vote.objects.create(
            user=user,
            link=self,
            alist=alist
        )
        vote.save()

        if user.pk is not self.author.pk:
            # add karma to link author if not voter
            from resrc.utils.karma import karma_rate
            karma_rate(self.author.pk, 1)

    def unvote(self, user):
        from resrc.vote.models import Vote
        Vote.objects.get(user=user, link=self).delete()

        if user.pk is not self.author.pk:
            # remove karma from link author if not voter
            from resrc.utils.karma import karma_rate
            karma_rate(self.author.pk, -1)

    def get_votes(self):
        from resrc.vote.models import Vote
        return Vote.objects.filter(link=self).count()

    def get_categories(self):
        categories = ['book', 'tutorial', 'interactive tutorial', 'guide',
            'resource', 'cheat sheet', 'article', 'blog', 'reference',
            'documentation', 'course', 'slides', 'video', 'MOOC', 'talk']
        cats = []
        for tag in self.tags.all().values_list('name', flat=True):
            if tag in categories:
                cats.append(tag)
        if cats:
            return "(%s)" % "/".join(cats)
        else:
            return ""


class RevisedLink(models.Model):
    link = models.ForeignKey('link.Link')
    title = models.CharField('title', max_length=120, null=True, blank=True)
    url = models.URLField('url', null=True, blank=True)
    level = models.CharField('Level', max_length=30, choices=zip(LEVELS, LEVELS), null=True, blank=True)
    language = models.ForeignKey('language.Language', null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "link %d - %s" % (self.link.pk, self.link.title)
