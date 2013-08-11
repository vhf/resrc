# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="tag-index"),
    url(r'^(?P<tag_slug>.+)/$', views.single, name="tag-single-slug"),
)
