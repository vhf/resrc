# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate

from resrc.link.tests.factories import LinkFactory
from resrc.tests.factories import UserFactory


class LinkViewTestCase(TestCase):

    def test_single_view(self):
        link = LinkFactory()
        link.save()
        resp = self.client.get(reverse('link-single', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse('link-single', kwargs={'link_pk': 77}))
        self.assertEqual(resp.status_code, 404)

    def test_single_slug_view(self):
        link = LinkFactory()
        link.save()
        resp = self.client.get(reverse('link-single-slug', kwargs={'link_pk': link.pk, 'link_slug': link.slug}))
        self.assertEqual(resp.status_code, 200)

        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')
        resp = self.client.get(reverse('link-single-slug', kwargs={'link_pk': link.pk, 'link_slug': link.slug}))
        self.assertEqual(resp.status_code, 200)


        resp = self.client.get(reverse('link-single-slug', kwargs={'link_pk': link.pk, 'link_slug': link.slug + "x"}))
        self.assertEqual(resp.status_code, 404)

    def test_new_link_view(self):
        resp = self.client.get(reverse('new-link'))
        self.assertEqual(resp.status_code, 302)

        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')
        resp = self.client.get(reverse('new-link'))
        self.assertEqual(resp.status_code, 200)
