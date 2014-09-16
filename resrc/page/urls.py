# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
from django.contrib.admin.views.decorators import staff_member_required

import views

urlpatterns = patterns(
    '',

    url(r'^about$', cache_page(60*60)(views.AboutView.as_view()), name="page-about"),
    url(r'^search$', views.SearchView.as_view(), name="page-search"),
    url(r'^search/(?P<tags>[^/]*)%(?P<operand>[^/]*)%(?P<excludes>[^/]*)$', views.SearchView.as_view()),
    url(r'^revision$', staff_member_required(views.RevisionView.as_view()), name="page-revision"),
    url(r'^dead$', staff_member_required(views.DeadView.as_view()), name="page-dead"),
)
