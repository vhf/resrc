# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate

from resrc.link.tests.factories import LinkFactory
from resrc.list.tests.factories import ListFactory
from resrc.tests.factories import UserFactory


class ListViewTestCase(TestCase):

    def test_single_view(self):
        alist = ListFactory()
        alist.save()
        resp = self.client.get(reverse('list-single', kwargs={'list_pk': alist.pk}))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse('list-single', kwargs={'list_pk': 77}))
        self.assertEqual(resp.status_code, 404)

    def test_single_slug_view(self):
        alist = ListFactory()
        alist.save()
        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': alist.slug}))
        self.assertEqual(resp.status_code, 200)

        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')
        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': alist.slug}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': alist.slug + "x"}))
        self.assertEqual(resp.status_code, 404)

    def test_new_list_view(self):
        resp = self.client.get(reverse('new-list'))
        self.assertEqual(resp.status_code, 302)

        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')
        resp = self.client.get(reverse('new-list'))
        self.assertEqual(resp.status_code, 200)
