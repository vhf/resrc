"""Admin objects for the ``feedback_form`` app."""
from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    """Admin class for the ``Feedback`` model."""
    list_display = [
        'creation_date', 'user_email', 'current_url', 'message_excerpt', ]
    list_filter = ['creation_date', 'current_url', ]
    date_hierarchy = 'creation_date'
    search_fields = ['user__email', 'email', 'current_url', 'message', ]

    def message_excerpt(self, obj):
        return truncatewords(obj.message, 10)
    message_excerpt.short_description = _('Message excerpt')

    def user_email(self, obj):
        if obj.user:
            return obj.user.email
        return obj.email
    user_email.short_description = _('Email')


admin.site.register(Feedback, FeedbackAdmin)
