# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from models import Profile


class SimpleTest(TestCase):

    def test_index(self):
        resp = self.client.get(reverse('resrc.userprofile.views.index'))
        self.assertEqual(resp.status_code, 200)

    def test_details(self):
        user = G(User, username='testuser')
        profile = G(Profile, user=user)

        resp = self.client.get(reverse('resrc.userprofile.views.details',
                               args=[user.username]))
        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        resp = self.client.get(reverse('resrc.userprofile.views.register_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.get(reverse('resrc.userprofile.views.login_view'))
        self.assertEqual(resp.status_code, 200)
