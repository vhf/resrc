# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse

from resrc.link.tests.factories import LinkFactory
from resrc.userprofile.tests.factories import ProfileFactory
from taggit.models import Tag

class TagViewTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user

        self.profile2 = ProfileFactory()
        self.user2 = self.profile2.user

        tag1 = Tag.objects.create(name='Ruby')
        tag1.save()
        tag2 = Tag.objects.create(name='Python')
        tag2.save()


    def test_single_view(self):
        resp = self.client.get(reverse('tag-single-slug', kwargs={'tag_slug': 'php'}))
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get(reverse('tag-single-slug', kwargs={'tag_slug': 'ruby'}))
        self.assertEqual(resp.status_code, 200)


    def test_index_view(self):
        resp = self.client.get(reverse('tag-index'))
        self.assertEqual(resp.status_code, 200)


    def test_tokeninput_json(self):
        resp = self.client.get(reverse('tokeninput-json'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/tag/searchq?q=r')
        self.assertEqual(resp.status_code, 200)


    def test_search_view(self):
        link = LinkFactory()
        link.author = self.user
        link.save()
        resp = self.client.get(reverse('tags-search', kwargs={
            'tags': 'Ruby,Python',
            'operand': 'or',
            'excludes': ''
        }))
        resp = self.client.get(reverse('tags-search', kwargs={
            'tags': '',
            'operand': 'or',
            'excludes': ''
        }))
        self.assertEqual(resp.status_code, 200)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('tags-search', kwargs={
            'tags': 'Ruby,Python',
            'operand': 'and',
            'excludes': ''
        }))
        self.assertEqual(resp.status_code, 200)


    def test_related(self):
        resp = self.client.get(reverse('tags-related', kwargs={'tags': 'Python'}))
        self.assertEqual(resp.status_code, 200)

