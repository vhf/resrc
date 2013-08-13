# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.http import Http404

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

    def test_ajax_add_to_list_or_create(self):
        import simplejson
        resp = self.client.get(reverse('ajax-add-to-list-or-create'))
        # not authenticated
        self.assertEqual(resp.content, simplejson.dumps({'result': 'fail'}))
        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')

        # authenticated but no post data
        resp = self.client.get(reverse('ajax-add-to-list-or-create'))
        self.assertEqual(resp.content, simplejson.dumps({'result': 'fail'}))

        link = LinkFactory()
        link.save()
        link2 = LinkFactory()
        link2.title = 'new link'
        link2.save()

        # authenticated and posting fake content
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            't': 'haxx0r',
        })
        self.assertEqual(resp.status_code, 404)

        # authenticated and adding link to default nonexistant bookmark list
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            't': 'bookmark',
        })
        self.assertEqual(resp.content, simplejson.dumps({'result': 'added'}))


        # authenticated and adding link to default existing bookmark list
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link2.pk,
            't': 'bookmark',
        })
        self.assertEqual(resp.content, simplejson.dumps({'result': 'added'}))

        # authenticated and adding link to default nonexistant reading list
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            't': 'toread',
        })
        self.assertEqual(resp.content, simplejson.dumps({'result': 'added'}))

        # authenticated and adding link to default existing reading list
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link2.pk,
            't': 'toread',
        })
        self.assertEqual(resp.content, simplejson.dumps({'result': 'added'}))

        # authenticated and removing link from default existing reading list
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link2.pk,
            't': 'toread',
        })
        self.assertEqual(resp.content, simplejson.dumps({'result': 'removed'}))

        # authenticated and adding/remove link to un/existing own list list
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            'ls': 43212234
        })
        self.assertEqual(resp.status_code, 404)

        alist = ListFactory()
        alist.save()
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            'ls': alist.pk
        })
        self.assertEqual(resp.content, simplejson.dumps({'result': 'added'}))
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            'ls': alist.pk
        })
        self.assertEqual(resp.content, simplejson.dumps({'result': 'removed'}))


    def test_ajax_own_lists(self):
        link = LinkFactory()
        link.save()
        link_pk = link.pk
        resp = self.client.get(reverse('ajax-own-lists', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 404)
        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')
        resp = self.client.get(reverse('ajax-own-lists', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 200)
