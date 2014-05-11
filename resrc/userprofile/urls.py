# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, url

from resrc.userprofile import views
from resrc.list import views as v

urlpatterns = patterns(
    '',
    url(r'^user/(?P<user_name>.+)/lists$', v.my_lists, name="user-lists"),
    url(r'^user/(?P<user_name>.+)$', views.details, name="user-url"),
    url(r'^edit$', views.settings_profile, name="user-settings"),
    url(r'^account$', views.settings_account, name="user-account"),
    url(r'^login$', views.login_view, name="user-login"),
    url(r'^modal/login$', views.login_view, {"modal": True}, name="user-login-modal"),
    url(r'^register$', views.register_view, name="user-register"),
    url(r'^register/success$', views.register_success, name="user-register-success"),
    url(r'^logout$', views.logout_view, name="user-logout"),
    url(r'^$', views.user_list, name="user-list"),
)
