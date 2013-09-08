"""Tests for the models of the ``feedback_form`` app."""
from django.test import TestCase

from ..models import Feedback


class FeedbackTestCase(TestCase):
    """Tests for the ``Feedback`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test if the ``Feedback`` model instantiates."""
        feedback = Feedback()
        self.assertTrue(feedback, msg='Should be correctly instantiated.')
