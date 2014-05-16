from django.test import TestCase
from resrc.userprofile.tests.factories import UserFactory, ProfileFactory


class UserprofileTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user
