from django.test import TestCase
from resrc.userprofile.tests.factories import UserFactory, ProfileFactory

from resrc.link.tests.factories import LinkFactory

from resrc.link.models import Link


class UserprofileTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user

        self.profile2 = ProfileFactory()
        self.user2 = self.profile2.user

    def test_slug(self):
        """test link slug"""
        link = LinkFactory()
        link.author_id = self.user.pk
        link.save()
        self.assertEqual(link.do_unique_slug(), False)
        self.assertEqual(
            link.slug, 'single-page-simple-comprehensive-overview-of-javascript')

        link = LinkFactory()
        link.author_id = self.user.pk
        link.save()
        self.assertEqual(
            link.slug, 'single-page-simple-comprehensive-overview-of-javascript-1')

    def test_lang(self):
        link = LinkFactory()
        link.author_id = self.user.pk
        self.assertEqual(link.get_lang(), 'English')

    def test_get_votes(self):
        user = UserFactory()
        user.save()
        profile = ProfileFactory()
        profile.user = user
        profile.save()
        link = LinkFactory()
        link.author_id = user.pk
        self.assertEqual(link.get_votes(), 0)

        link.vote(user)
        self.assertEqual(link.get_votes(), 1)

        link.unvote(user)
        self.assertEqual(link.get_votes(), 0)

    def test_categories(self):
        link = LinkFactory.create(True, ("article"))
        link.author_id = self.user.pk
        link.save()
        self.assertEqual(link.get_categories(), "")

