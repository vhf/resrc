import factory

from resrc.link.models import Link
from resrc.tests.factories import UserFactory

class LinkFactory(factory.Factory):
    FACTORY_FOR = Link

    title = "Single page, Simple, Comprehensive Overview of Javascript"
    url = "http://betterexplained.com/articles/the-single-page-javascript-overview/"
    author = factory.SubFactory(UserFactory)

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
