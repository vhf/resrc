from django.test import TestCase
from resrc.userprofile.tests.factories import UserFactory, ProfileFactory
from resrc.link.tests.factories import LinkFactory
from resrc.list.tests.factories import ListFactory

class UserprofileTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user
        self.list = ListFactory()
        self.link = LinkFactory()


    def model_test(self):
        self.list.save()
        self.assertTrue(self.list.pk)

        self.list.delete()
        self.assertEqual(self.list.pk, None)
