# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',

    url(r'^faq$', views.faq, name="page-faq"),
    url(r'^about$', views.about, name="page-about"),

    url(r'^$', views.home, name="page-home"),
)
