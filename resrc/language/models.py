# -*- coding: utf-8 -*-:
from django.conf import settings
from django.db import models

class Language(models.Model):
    language = models.CharField(max_length=7, choices=settings.LANGUAGES)

    def __unicode__(self):
        from django.conf import settings
        return [x[1] for x in settings.LANGUAGES if x[0] == self.language][0]
