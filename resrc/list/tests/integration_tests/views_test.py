# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse

from resrc.link.tests.factories import LinkFactory
from resrc.userprofile.tests.factories import ProfileFactory
from resrc.list.tests.factories import ListFactory
from resrc.list.models import List
from django.core.cache import cache
import json
from resrc.language.models import Language


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
        cache.delete('tags_csv')

        resp = self.client.get(reverse('list-single', kwargs={'list_pk': alist.pk}))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse('list-single', kwargs={'list_pk': 1337}))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': alist.slug}))
        self.assertEqual(resp.status_code, 200)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': alist.slug}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': 'something'}))
        self.assertEqual(resp.status_code, 404)

        alist.owner = self.user2
        alist.is_public = False
        alist.save()
        resp = self.client.get(reverse('list-single-slug', kwargs={'list_pk': alist.pk, 'list_slug': alist.slug}))
        self.assertEqual(resp.status_code, 403)

    def test_delete_list(self):
        alist = ListFactory()
        alist.owner = self.user
        alist.save()

        resp = self.client.post(reverse('list-delete', kwargs={'list_pk': alist.pk}), {})
        self.assertEqual(resp.status_code, 302)

        self.client.login(username=self.user2.username, password='test123')
        resp = self.client.get(reverse('list-delete', kwargs={'list_pk': alist.pk}))
        self.assertEqual(resp.status_code, 403)

        resp = self.client.post(reverse('list-delete', kwargs={'list_pk': alist.pk}), {})
        self.assertEqual(resp.status_code, 404)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.post(reverse('list-delete', kwargs={'list_pk': alist.pk}), {})
        self.assertEqual(resp.status_code, 302)


    def test_ajax_add_to_list_or_create(self):
        resp = self.client.get(reverse('ajax-add-to-list-or-create'))
        self.assertEqual(resp.content, json.dumps({'result': 'fail'}))

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('ajax-add-to-list-or-create'))
        self.assertEqual(resp.content, json.dumps({'result': 'fail'}))

        link = LinkFactory()
        link.author = self.user
        link.save()
        cache.delete('link_%s' % link.pk)
        alist = ListFactory()
        alist.owner = self.user
        alist.save()
        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            'ls': alist.pk
        })
        self.assertEqual(resp.content, json.dumps({'result': 'added'}))

        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            'ls': alist.pk
        })
        self.assertEqual(resp.content, json.dumps({'result': 'removed'}))

        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            't': 'toread'
        })
        self.assertEqual(resp.content, json.dumps({'result': 'added'}))

        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            't': 'bookmark'
        })
        self.assertEqual(resp.content, json.dumps({'result': 'added'}))

        resp = self.client.post(reverse('ajax-add-to-list-or-create'), {
            'lk': link.pk,
            't': 'something'
        })
        self.assertEqual(resp.status_code, 404)


    def test_ajax_own_list(self):
        link = LinkFactory()
        link.author = self.user
        link.save()

        resp = self.client.get(reverse('ajax-own-lists', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 403)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('ajax-own-lists', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 200)


    def test_ajax_create_list(self):
        link = LinkFactory()
        link.author = self.user
        link.save()
        cache.delete('link_%s' % link.pk)

        resp = self.client.get(reverse('ajax-create-list', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 403)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('ajax-create-list', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 403)

        resp = self.client.post(reverse('ajax-create-list', kwargs={'link_pk': link.pk}), {
            'title': 'My list',
            'description': 'something',
            'private': True,
            'language': 'en'
        })
        self.assertEqual(resp.content, json.dumps({'result': 'success'}))

        resp = self.client.post(reverse('ajax-create-list', kwargs={'link_pk': link.pk}), {
            'title': 'My list',
            'description': 'something'
        })
        self.assertEqual(resp.content, json.dumps({'result': 'invalid'}))


    def test_new_list(self):
        resp = self.client.get(reverse('new-list'))
        self.assertEqual(resp.status_code, 302)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('new-list'))
        self.assertEqual(resp.status_code, 200)


        resp = self.client.post(reverse('new-list'), {
            'title': 'My list',
            'description': 'something',
            'private': True,
            'language': 'en',
            'url': '',
            'mdcontent': '#lala'
        })

        self.assertEqual(List.objects.get(title='My list').is_public, False)


    def test_edit_list(self):
        alist = ListFactory()
        alist.title = 'My list 2'
        alist.owner = self.user
        alist.language = Language.objects.create(language='en', name='English')
        alist.save()

        resp = self.client.get(reverse('list-edit', kwargs={'list_pk': alist.pk}))
        self.assertEqual(resp.status_code, 302)

        self.client.login(username=self.user2.username, password='test123')
        resp = self.client.get(reverse('list-edit', kwargs={'list_pk': alist.pk}))
        self.assertEqual(resp.status_code, 403)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('list-edit', kwargs={'list_pk': alist.pk}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse('list-edit', kwargs={'list_pk': alist.pk}), {
            'title': 'My list 2',
            'description': 'something',
            'private': False,
            'language': 'en',
            'url': '',
            'mdcontent': '#lala'
        })
        self.assertEqual(List.objects.get(title='My list 2').description, 'something')
