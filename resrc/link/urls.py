# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.links_page, name="links"),
    url(r'^(?P<link_pk>\d+)/$', views.single, name="link-single"),
    url(r'^(?P<link_pk>\d+)/(?P<link_slug>.+)/$', views.single, name="link-single-slug"),
    url(r'^(?P<link_pk>\d+)/edit$', views.edit_link, name="link-edit"),
    url(r'^(?P<link_pk>\d+)/upvote$', views.ajax_upvote_link, name="link-upvote"),
    url(r'^(?P<link_pk>\d+)/suggest$', views.ajax_revise_link, name="revise-link"),
    url(r'^new/$', views.new_link, name="new-link"),
    url(r'^popup/(?P<title>.+)/u/(?P<url>.+)$', views.new_link, name="new-link-popup"),
)
