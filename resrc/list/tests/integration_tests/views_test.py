# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse

from resrc.link.tests.factories import LinkFactory
from resrc.userprofile.tests.factories import ProfileFactory
from resrc.list.tests.factories import ListFactory
from resrc.link.models import Link
from resrc.list.models import List


class LinkViewTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user

        self.profile2 = ProfileFactory()
        self.user2 = self.profile2.user


    def test_lists_page(self):
        resp = self.client.get(reverse('lists'))
        self.assertEqual(resp.status_code, 200)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('lists'))
        self.assertEqual(resp.status_code, 200)


    def test_single_list(self):
        alist = ListFactory()
        alist.owner = self.user
        alist.save()

        resp = self.client.get(reverse('list-single', kwargs={'list_pk': alist.pk}))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse('list-single', kwargs={'list_pk': 1337}))
        self.assertEqual(resp.status_code, 404)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': alist.slug}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': 'something'}))
        self.assertEqual(resp.status_code, 404)

        alist.owner = self.user2
        alist.is_public = False
        alist.save()
        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': alist.slug}))
        self.assertEqual(resp.status_code, 404)
