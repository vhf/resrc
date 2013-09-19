# -*- coding: utf-8 -*-:
from django.db import models
from django.conf import settings

class Language(models.Model):
    language = models.CharField(max_length=7, choices=settings.LANGUAGES)
