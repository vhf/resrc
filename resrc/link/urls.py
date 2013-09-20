# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^(?P<link_pk>\d+)/$', views.single, name="link-single"),
    url(r'^(?P<link_pk>\d+)/(?P<link_slug>.+)/$', views.single, name="link-single-slug"),
    url(r'^(?P<link_pk>\d+)/edit$', views.edit_link, name="link-edit"),
    url(r'^new/$', views.new_link, name="new-link"),
    url(r'^button/$', views.new_link_button, name="new-link-button"),
    url(r'^button/(?P<title>.+)/u/(?P<url>.+)$', views.new_link_button),
)
