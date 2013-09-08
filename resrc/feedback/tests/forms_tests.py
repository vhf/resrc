"""Tests for the forms of the ``feedback_form`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from mailer.models import Message

from ..forms import FeedbackForm
from ..models import Feedback


class FeedbackFormTestCase(TestCase):
    """Test for the ``FeedbackForm`` form class."""
    longMessage = True

    def test_form(self):
        data = {
            'feedback-email': 'test@example.com',
            'feedback-message': 'Foo',
            'feedback-url': 'http://www.example.com',
        }
        form = FeedbackForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Message.objects.all().count(), 0)
        self.assertEqual(Feedback.objects.all().count(), 0)

        # Valid post
        data.update({'feedback-url': ''})
        form = FeedbackForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Message.objects.all().count(), 1)
        self.assertEqual(Feedback.objects.all().count(), 1)
        self.assertEqual(Feedback.objects.all()[0].message, 'Foo')
        self.assertEqual(Feedback.objects.all()[0].email, 'test@example.com')
        Feedback.objects.all()[0].delete()
        Message.objects.all()[0].delete()

        # Valid post with user account
        user = UserFactory()
        data.update({'feedback-email': ''})
        form = FeedbackForm(data=data, user=user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Message.objects.all().count(), 1)
        self.assertEqual(Feedback.objects.all().count(), 1)
        self.assertEqual(Feedback.objects.all()[0].message, 'Foo')
        self.assertEqual(Feedback.objects.all()[0].user, user)
