"""URLs for the ``feedback_form`` app."""
from django.conf.urls.defaults import patterns, url

from .views import FeedbackCreateView


urlpatterns = patterns(
    '',
    url(r'', FeedbackCreateView.as_view(), name='feedback_form'),
)
