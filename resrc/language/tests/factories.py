import factory
from resrc.language.models import Language


class LanguageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Language

    language = "en"
    name = "English"
