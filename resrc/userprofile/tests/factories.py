from django.contrib.auth.models import User, Permission
import factory

from resrc.userprofile.models import Profile
from resrc.language.tests.factories import LanguageFactory

# Don't try to directly use UserFactory, this didn't create Profile then don't work!
class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = 'test123'

    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class ProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Profile

    user = factory.SubFactory(UserFactory)
    about = "About me"
    karma = 0
    show_email = True
