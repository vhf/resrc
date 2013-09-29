# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.lists_page, name="lists"),
    url(r'^(?P<list_pk>\d+)/$', views.single, name="list-single"),
    url(r'^(?P<list_pk>\d+)/upvote$', views.ajax_upvote_list, name="list-upvote"),
    url(r'^edit/(?P<list_pk>\d+)$', views.edit, name="list-edit"),
    url(r'^delete/(?P<list_pk>\d+)$', views.delete, name="list-delete"),
    url(r'^delete/(?P<list_pk>\d+)/toobad$', views.delete, {"confirm": True}, name="list-delete-confirmed"),
    url(r'^(?P<list_pk>\d+)/(?P<list_slug>.+)/$', views.single, name="list-single-slug"),
    url(r'^a/(?P<link_pk>\d+)/$', views.ajax_own_lists, name="ajax-own-lists"),
    url(r'^c/(?P<link_pk>\d+)/$', views.ajax_create_list, name="ajax-create-list"),
    url(r'^new/$', views.new_list, name="new-list"),

    url(r'^add_default/$', views.ajax_add_to_list_or_create,
        name="ajax-add-to-list-or-create")
)
