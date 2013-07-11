# coding: utf-8

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import page.views
import settings

urlpatterns = patterns(
    '',
    url(r'^u/',  include('resrc.user.urls')),
    url(r'^lk/', include('resrc.link.urls')),
#    url(r'^ls/', include('resrc.list.urls')),
    url(r'^p/',  include('resrc.page.urls')),
    url(r'^a/',  include(admin.site.urls)),

    url(r'^captcha/', include('captcha.urls')),

    url(r'^$', page.views.home),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
