# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',

    url(r'^about$', views.about, name="page-about"),
    url(r'^search$', views.search, name="page-search"),
    url(r'^search/(?P<tags>[^/]*)%(?P<operand>[^/]*)%(?P<excludes>[^/]*)$', views.search),
    url(r'^revision$', views.revision, name="page-revision"),
    url(r'^dead$', views.dead, name="page-dead"),
)
