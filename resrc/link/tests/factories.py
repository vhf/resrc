import factory

from resrc.link.models import Link
from resrc.userprofile.tests.factories import UserFactory
from resrc.language.tests.factories import LanguageFactory
from taggit.models import Tag


class LinkFactory(factory.Factory):
    FACTORY_FOR = Link

    title = "Single page, Simple, Comprehensive Overview of Javascript"
    url = "http://betterexplained.com/articles/the-single-page-javascript-overview/"
    author = factory.SubFactory(UserFactory)
    language = factory.SubFactory(LanguageFactory)
    level = 'beginner'
