# -*- coding: utf-8 -*-:
from django.db import models
from django.conf import settings


class Language(models.Model):
    language = models.CharField(max_length=7, choices=settings.LANGUAGES)


class Vote(models.Model):
    from resrc.link.models import Link
    from resrc.list.models import List
    from django.contrib.auth.models import User
    user = models.ForeignKey(User, verbose_name='user')
    alist = models.ForeignKey(List, null=True, blank=True)
    link = models.ForeignKey(Link, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
