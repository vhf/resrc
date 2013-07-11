from django.db import models

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Link(models.Model):

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    title = models.CharField('title', max_length=120)

    url = models.URLField('url')

    pubdate = models.DateTimeField('date added', auto_now_add=True)

    author = models.ForeignKey(User, verbose_name='author')

    upvotes = models.IntegerField('upvotes', null=True, blank=True)
    downvotes = models.IntegerField('downvotes', null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/lk/{0}/{1}'.format(self.pk, slugify(self.title))
