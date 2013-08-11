# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from resrc.userprofile.models import Profile


class SimpleTest(TestCase):

    def test_user_list(self):
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(resp.status_code, 200)

    def test_details(self):
        user = G(User, username='testuser')
        profile = G(Profile, user=user)

        resp = self.client.get(reverse('user-url', args=[user.username]))
        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        resp = self.client.get(reverse('user-register'))
        self.assertEqual(resp.status_code, 200)
