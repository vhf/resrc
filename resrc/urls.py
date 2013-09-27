# -*- coding: utf-8 -*-:
from django.conf.urls import patterns, include, url
# from django.contrib import admin

# admin.autodiscover()

from page.views import home
from tag.views import search
import settings

urlpatterns = patterns(
    '',
    url(r'^user/',  include('resrc.userprofile.urls')),
    url(r'^link/', include('resrc.link.urls')),
    url(r'^list/', include('resrc.list.urls')),
    url(r'^page/',  include('resrc.page.urls')),
    url(r'^tag/',  include('resrc.tag.urls')),
    url(r'^search/(?P<tags>[^/]*)/(?P<operand>[^/]*)/(?P<excludes>[^/]*)/$', search, name="search"),
#    url(r'^a/',  include(admin.site.urls)),

    # third party includes
    url(r'^ca/', include('captcha.urls')),
    url(r'^comment/', include('mptt_comments.urls')),

    url(r'^$', home, name="home"),

    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
         'document_root': settings.MEDIA_ROOT}),
    )
