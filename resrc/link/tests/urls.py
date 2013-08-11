from django.conf.urls import *

urlpatterns = patterns(
    '',
    url(r'^$', include('resrc.urls')),
)
