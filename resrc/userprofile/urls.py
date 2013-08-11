# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^user/(?P<user_name>.+)$', views.details, name="user-url"),
    url(r'^edit$', views.settings_profile, name="user-settings"),
    url(r'^account$', views.settings_account, name="user-account"),
    url(r'^login$', views.login_register_view, name="user-login"),
    url(r'^register$', views.login_register_view, {"register": True}, name="user-register"),
    url(r'^logout$', views.logout_view, name="user-logout"),
    url(r'^$', views.user_list, name="user-list"),
)
