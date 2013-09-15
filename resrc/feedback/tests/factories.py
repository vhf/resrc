"""Factories of the ``feedback`` app."""
import factory

from ..models import Feedback


class FeedbackFactory(factory.Factory):
    FACTORY_FOR = Feedback

    message = 'Test Message'
