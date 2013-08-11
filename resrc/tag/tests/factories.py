import factory

from taggit.models import Tag
from resrc.tests.factories import UserFactory


class TagFactory(factory.Factory):
    FACTORY_FOR = Tag

    name = "Django"
