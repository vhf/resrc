# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',

    url(r'^faq$', views.faq),
    url(r'^about$', views.about),
    url(r'^test$', views.test),

    url(r'^$', views.index),
)
