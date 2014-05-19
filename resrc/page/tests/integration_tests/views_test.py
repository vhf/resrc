# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse

from resrc.userprofile.tests.factories import ProfileFactory


class PageViewTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user

        self.profile2 = ProfileFactory()
        self.user2 = self.profile2.user


    def test_about_view(self):
        resp = self.client.get(reverse('page-about'))
        self.assertEqual(resp.status_code, 200)


    def test_search_view(self):
        resp = self.client.get(reverse('page-search'))
        self.assertEqual(resp.status_code, 200)


    def test_home_view(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)


    def test_revision_view(self):
        resp = self.client.get(reverse('page-revision'))
        self.assertEqual(resp.status_code, 403)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('page-revision'))
        self.assertEqual(resp.status_code, 403)

        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('page-revision'))
        self.assertEqual(resp.status_code, 200)
