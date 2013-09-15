"""Forms for the ``feedback`` app."""
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

from django_libs.utils_email import send_email

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    A feedback form with modern spam protection.

    :url: Field to trap spam bots.

    """
    url = forms.URLField(required=False)

    def __init__(self, user=None, url=None, *args, **kwargs):
        super(FeedbackForm, self).__init__(prefix='feedback', *args, **kwargs)
        if url:
            self.instance.current_url = url
        if user:
            self.instance.user = user
            del self.fields['email']
        else:
            self.fields['email'].required = True

    def save(self):
        if not self.cleaned_data.get('url'):
            obj = super(FeedbackForm, self).save()
            send_email(
                '',
                {
                    'url': reverse('admin:feedback_feedback_change',
                                   args=(obj.id, )),
                    'email': obj.user or obj.email,
                    'date': obj.creation_date,
                    'message': obj.message,
                },
                'feedback/email/subject.html',
                'feedback/email/body.html',
                'feedback/email/body_plain.html',
                from_email=settings.FROM_EMAIL,
                recipients=[manager[1] for manager in settings.MANAGERS],
            )
            return obj

    class Media:
        css = {'all': ('feedback/css/feedback.css'), }
        js = ('feedback/js/feedback.js', )

    class Meta:
        model = Feedback
        fields = ('email', 'message')
