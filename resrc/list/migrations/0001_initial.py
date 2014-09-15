# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
        ('link', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20140915_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80, verbose_name=b'title')),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField(verbose_name=b'description')),
                ('md_content', models.TextField(verbose_name=b'md_content')),
                ('html_content', models.TextField(verbose_name=b'html_content')),
                ('url', models.URLField(null=True, verbose_name=b'url', blank=True)),
                ('is_public', models.BooleanField(default=True)),
                ('pubdate', models.DateField(auto_now_add=True)),
                ('views', models.IntegerField(default=0)),
                ('language', models.ForeignKey(default=1, to='language.Language')),
            ],
            options={
                'verbose_name': 'List',
                'verbose_name_plural': 'Lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adddate', models.DateField(auto_now_add=True)),
                ('alist', models.ForeignKey(to='list.List')),
                ('links', models.ForeignKey(to='link.Link')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='list',
            name='links',
            field=models.ManyToManyField(to='link.Link', through='list.ListLinks'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='list',
            name='owner',
            field=models.ForeignKey(related_name=b'list_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='list',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
