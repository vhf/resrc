"""Settings of the ``feedback_form``` application."""
from django.conf import settings


FEEDBACK_FORM_COLOR = getattr(settings, 'FEEDBACK_FORM_COLOR', '#6caec9')
FEEDBACK_FORM_TEXTCOLOR = getattr(settings, 'FEEDBACK_FORM_TEXTCOLOR', '#fff')
FEEDBACK_FORM_TEXT = getattr(settings, 'FEEDBACK_FORM_TEXT', '')
