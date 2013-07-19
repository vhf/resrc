# -*- coding: utf-8 -*-:
from hashlib import md5

from django.db import models
from django.contrib.auth.models import User

from resrc.link.models import Link
from resrc.list.models import List


class Profile(models.Model):

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    user = models.ForeignKey(User, unique=True, verbose_name='user')

    about = models.TextField('about', blank=True)

    karma = models.IntegerField('karma', null=True, blank=True)

    show_email = models.BooleanField(default=False)

    favs = models.ManyToManyField(
        Link, related_name="%(app_label)s_%(class)s_related")

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return '/u/user/{0}'.format(self.user.username)


    # Links
    def get_links(self):
        return Link.objects.all().filter(owner__pk=self.user.pk)

    def get_link_count(self):
        return self.get_links().count()

    # Lists
    def get_lists(self):
        return List.objects.filter(owner__pk=self.user.pk)

    def get_list_count(self):
        return self.get_lists().count()

    def get_public_lists(self):
        return self.get_lists().filter(is_public=True)

    def get_private_lists(self):
        return self.get_tutorials().filter(is_public=False)
