"""Models for the ``feedback_form`` app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Feedback(models.Model):
    """
    Holds information about one user feedback.

    :user: User account of the poster, if logged in.
    :email: Email field, if user isn't logged in and wants to send her email.
    :current_url: URL of the current page.
    :message: Feedback text.
    :creation_date: Datetime of the feedback creation.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='feedback_form_submissions',
        blank=True, null=True,
    )

    email = models.EmailField(
        verbose_name=_('Email'),
        blank=True,
    )

    current_url = models.URLField(
        verbose_name=_('Current URL'),
        max_length=50,
        blank=True,
    )

    message = models.TextField(
        verbose_name=_('Message'),
        max_length=4000,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation Date'),
    )

    class Meta:
        ordering = ['-creation_date']

    def __unicode__(self):
        if self.user:
            return '{0} - {1}'.format(self.creation_date, self.user)
        elif self.email:
            return '{0} - {1}'.format(self.creation_date, self.email)
        return '{0}'.format(self.creation_date)
