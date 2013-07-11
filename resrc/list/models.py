from django.db import models


class List(models.Model):

    class Meta:
        verbose_name = 'List'
        verbose_name_plural = 'Lists'

    title = models.CharField('title', max_length=80)
