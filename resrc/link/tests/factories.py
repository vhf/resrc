import factory

from resrc.link.models import Link
from resrc.userprofile.tests.factories import UserFactory
from resrc.language.tests.factories import LanguageFactory
from taggit.models import Tag


class LinkFactory(factory.Factory):
    FACTORY_FOR = Link

    title = factory.Sequence(lambda n: 'Example #{0}'.format(n))
    url = factory.Sequence(lambda n: 'http://example.com/{0}'.format(n))
    author = factory.SubFactory(UserFactory)
    language = factory.SubFactory(LanguageFactory)
    level = 'beginner'
