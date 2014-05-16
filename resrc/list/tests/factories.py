import factory

from resrc.list.models import List
from resrc.userprofile.tests.factories import UserFactory

class ListFactory(factory.Factory):
    FACTORY_FOR = List

    title = "My own public list"
    owner = factory.SubFactory(UserFactory)
