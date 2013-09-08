"""Template tags and filters for the ``feedback_form`` app."""
from django import template

from ..app_settings import *  # NOQA
from ..forms import FeedbackForm

register = template.Library()


@register.inclusion_tag('feedback_form/partials/form.html')
def feedback_form(path, user):
    return {
        'form': FeedbackForm(url=path, user=user),
        'background_color': FEEDBACK_FORM_COLOR,
        'text_color': FEEDBACK_FORM_TEXTCOLOR,
        'text': FEEDBACK_FORM_TEXT,
    }
