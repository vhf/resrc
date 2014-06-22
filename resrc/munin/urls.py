# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',

    url(r'^total_links/$', views.total_links),
    url(r'^total_lists/$', views.total_lists),
)
