# -*- coding: utf-8 -*-:
from django.test import TestCase
from django_dynamic_fixture import G

from django.contrib.auth.models import User
from resrc.tests.factories import UserFactory

from resrc.userprofile.models import Profile

from resrc.utils.templatetags.profile import profile
from resrc.utils.templatetags.gravatar import gravatar


class TemplateTagsTests(TestCase):

    def test_profile_none(self):
        '''Test the output of profile templatetag if profile does not exist'''
        user = G(User)
        self.assertEqual(None, profile(user))

    def test_profile_existing(self):
        '''Test the output of profile templatetag if profile does exist'''
        user = G(User)
        p = G(Profile, user=user)
        self.assertEqual(p, profile(user))

    def test_gravatar_default(self):
        user = UserFactory()
        user.save()
        p = G(Profile, user=user)
        p.email = 'foobar@example.com'
        p.save()
        self.assertEqual(gravatar(p.email), \
            '<img src="http://www.gravatar.com/avatar.php?size=80&gravatar_id=0d4907cea9d97688aa7a5e722d742f71" alt="gravatar" />')

        self.assertEqual(gravatar(p.email, 80, 'Hello'), \
            '<img src="http://www.gravatar.com/avatar.php?size=80&gravatar_id=0d4907cea9d97688aa7a5e722d742f71" alt="gravatar for Hello" />')
