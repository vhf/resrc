# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

import page.views
import settings

urlpatterns = patterns(
    '',
    url(r'^u/',  include('resrc.userprofile.urls')),
    url(r'^lk/', include('resrc.link.urls')),
    # url(r'^ls/', include('resrc.list.urls')),
    url(r'^p/',  include('resrc.page.urls')),
    url(r'^a/',  include(admin.site.urls)),

    # third party includes
    url(r'^ca/', include('captcha.urls')),
    url(r'^co/', include('mptt_comments.urls')),

    url(r'^$', page.views.home),

    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
         'document_root': settings.MEDIA_ROOT}),
    )
