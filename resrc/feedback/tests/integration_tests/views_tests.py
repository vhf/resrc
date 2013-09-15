"""Tests for the views of the ``feedback`` app."""
from django.test import TestCase

from resrc.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from ...models import Feedback


class FeedbackCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``FeedbackCreateView`` generic view."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()

    def get_view_name(self):
        return 'feedback'

    def test_view(self):
        self.should_be_callable_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='post', data={'feedback-message': 'Foo'})
        self.assertEqual(Feedback.objects.all().count(), 1)
        self.assertEqual(Feedback.objects.all()[0].message, 'Foo')
        self.assertEqual(Feedback.objects.all()[0].current_url, '/f/')

        # Test AJAX
        self.is_callable(method='post', data={'feedback-message': 'Foo'},
                         ajax=True)
        self.is_callable(ajax=True)
