import factory

from resrc.list.models import List
from resrc.tests.factories import UserFactory

class ListFactory(factory.Factory):
    FACTORY_FOR = List

    title = "My own public list"
    owner = factory.SubFactory(UserFactory)

    upvotes = 0
    votes_h00 = 0
    votes_h02 = 0
    votes_h04 = 0
    votes_h06 = 0
    votes_h08 = 0
    votes_h10 = 0
    votes_h12 = 0
    votes_h14 = 0
    votes_h16 = 0
    votes_h18 = 0
    votes_h20 = 0
    votes_h22 = 0
    score_h24 = 0

