"""Tests for the template tags and filters of the ``feedback`` app."""
from django.contrib.auth.models import AnonymousUser
from django.template import Template, RequestContext
from django.test import TestCase, RequestFactory

from resrc.tests.factories import UserFactory


class FeedbackFormTestCase(TestCase):
    """Tests for the ``feedback`` tag."""
    longMessage = True

    def test_render_tag(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        c = RequestContext(request)
        t = Template('{% load feedback_tags %}{% feedback request.path None %}')
        self.assertIn('<input type="submit" class="button small" value="Send Feedback" />',
                      t.render(c))
        # Should add the email field, because user is anonymous
        self.assertIn('email', t.render(c))

        # Test with logged in user
        request.user = UserFactory()
        c = RequestContext(request)
        t = Template('{% load feedback_tags %}{% feedback request.path request.user %}')
        self.assertIn('<input type="submit" class="button small" value="Send Feedback" />',
                      t.render(c))
