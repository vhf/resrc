"""Factories for models that are global to the project."""
from django.contrib.auth.models import User

import factory


class UserFactory(factory.Factory):
    """
    Creates a new ``User`` object.

    Username will be a random 30 character md5 value.
    Email will be ``userN@example.com`` with ``N`` being a counter.
    Password will be ``test123`` by default.

    """
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'username{0}'.format(n))
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = 'test123'
        if 'password' in kwargs:
            password = kwargs.pop('password')
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        user.set_password(password)
        if create:
            user.save()
        return user
