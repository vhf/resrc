# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="tag-index"),
    url(r'^tag/(?P<tag_slug>.+)/$', views.single, name="tag-single-slug"),
    url(r'^search/(?P<tags>[^/]*)%(?P<operand>[^/]*)%(?P<excludes>[^/]*)$', views.search, name="tags-search"),
    url(r'^related/(?P<tags>[^/]*)', views.related, name="tags-related"),

)
