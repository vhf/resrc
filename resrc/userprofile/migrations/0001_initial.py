# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=255)),
                ('about', models.TextField(verbose_name=b'about', blank=True)),
                ('karma', models.IntegerField(null=True, verbose_name=b'karma', blank=True)),
                ('show_email', models.BooleanField(default=False, verbose_name=b'show_email')),
                ('languages', models.ManyToManyField(to='language.Language')),
                ('user', models.ForeignKey(verbose_name=b'user', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
    ]
