"""Factories of the ``feedback_form`` app."""
import factory

from ..models import Feedback


class FeedbackFactory(factory.Factory):
    FACTORY_FOR = Feedback

    message = 'Test Message'
