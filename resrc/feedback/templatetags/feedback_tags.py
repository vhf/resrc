"""Template tags and filters for the ``feedback`` app."""
from django import template

from ..app_settings import *  # NOQA
from ..forms import FeedbackForm

register = template.Library()


@register.inclusion_tag('feedback/partials/form.html')
def feedback(path, user):
    return {
        'form': FeedbackForm(url=path, user=user),
        'text': FEEDBACK_FORM_TEXT,
    }
