"""Tests for the template tags and filters of the ``feedback_form`` app."""
from django.contrib.auth.models import AnonymousUser
from django.template import Template, RequestContext
from django.test import TestCase, RequestFactory

from django_libs.tests.factories import UserFactory


class FeedbackFormTestCase(TestCase):
    """Tests for the ``feedback_form`` tag."""
    longMessage = True

    def test_render_tag(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        c = RequestContext(request)
        t = Template('{% load feedback_tags %}{% feedback_form %}')
        self.assertIn('<input type="submit" value="Send Feedback" />',
                      t.render(c))
        # Should add the email field, because user is anonymous
        self.assertIn('email', t.render(c))

        # Test with logged in user
        request.user = UserFactory()
        c = RequestContext(request)
        self.assertIn('<input type="submit" value="Send Feedback" />',
                      t.render(c))
        self.assertNotIn('email', t.render(c))
