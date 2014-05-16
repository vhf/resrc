import factory

from resrc.link.models import Link
from resrc.tests.factories import UserFactory


class LinkFactory(factory.Factory):
    FACTORY_FOR = Link

    title = "Single page, Simple, Comprehensive Overview of Javascript"
    url = "http://betterexplained.com/articles/the-single-page-javascript-overview/"
    author = factory.SubFactory(UserFactory)
