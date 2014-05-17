from django.test import TestCase
from resrc.userprofile.tests.factories import UserFactory, ProfileFactory

from resrc.link.tests.factories import LinkFactory

from resrc.link.models import Link


class UserprofileTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user


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
