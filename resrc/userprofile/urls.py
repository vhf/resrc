# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^user/(?P<user_name>.+)$', views.details, name="user-url"),
    url(r'^edit$', views.settings_profile),
    url(r'^account$', views.settings_account),
    url(r'^login$', views.login_view),
    url(r'^register$', views.register_view),
    url(r'^logout$', views.logout_view),
    url(r'^$', views.user_list),
)
