"""Views for the ``feedback`` app."""
from django.core.urlresolvers import reverse
from django.views.generic import CreateView

from .app_settings import *  # NOQA
from .forms import FeedbackForm
from .models import Feedback


class FeedbackCreateView(CreateView):
    """View to display and handle a feedback create form."""
    model = Feedback
    form_class = FeedbackForm
    ajax_template = 'feedback/partials/form_content.html'

    def get_form_kwargs(self):
        kwargs = super(FeedbackCreateView, self).get_form_kwargs()
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        kwargs.update({
            'url': self.request.META.get('HTTP_REFERER', self.request.path)})
        return kwargs

    def get_template_names(self):
        if self.request.is_ajax():
            return self.ajax_template
        return super(FeedbackCreateView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(FeedbackCreateView, self).get_context_data(**kwargs)
        context.update({
            'text': FEEDBACK_FORM_TEXT,
        })
        return context

    def get_success_url(self):
        return reverse('feedback')
