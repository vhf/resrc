# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20140915_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120, verbose_name=b'title')),
                ('content', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(max_length=255)),
                ('url', models.URLField(verbose_name=b'url')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name=b'date added')),
                ('level', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Level', choices=[(b'beginner', b'beginner'), (b'intermediate', b'intermediate'), (b'advanced', b'advanced')])),
                ('flagged', models.BooleanField(default=False)),
                ('author', models.ForeignKey(verbose_name=b'author', to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(default=1, to='language.Language')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RevisedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120, null=True, verbose_name=b'title', blank=True)),
                ('url', models.URLField(null=True, verbose_name=b'url', blank=True)),
                ('level', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Level', choices=[(b'beginner', b'beginner'), (b'intermediate', b'intermediate'), (b'advanced', b'advanced')])),
                ('tags', models.CharField(max_length=255, null=True, blank=True)),
                ('language', models.ForeignKey(blank=True, to='language.Language', null=True)),
                ('link', models.ForeignKey(to='link.Link')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
