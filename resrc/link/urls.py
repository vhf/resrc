# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^(?P<link_pk>\d+)/(?P<link_slug>.+)/$', views.single),
)
