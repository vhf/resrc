# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate

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


    def test_new_link_post_view(self):
        self.client.login(username=self.user.username, password='test123')

        resp = self.client.post(reverse('new-link'), {
            'title': u'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'language': 'en',
            'level': 'beginner'
        })
        link = Link.objects.get(url="http://12devs.co.uk/articles/204/")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            link.title, 'Building static websites with Middleman, deploying to Heroku')

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'language': 'en',
            'level': 'beginner'
        })
        self.assertEqual(resp.status_code, 302)


    def test_new_link_ajax_view(self):
        self.client.login(username=self.user.username, password='test123')

        resp = self.client.post(reverse('new-link'), {
            'title': u'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'ajax': '1',
            'id': 91329123,
            'language': 'en',
            'level': 'beginner'
        })
        self.assertEqual(resp.status_code, 404)

        alist = ListFactory()
        alist.owner = self.user
        alist.save()
        alist = List.objects.get(owner=self.user)
        link = Link.objects.get(url="http://12devs.co.uk/articles/204/")

        resp = self.client.post(reverse('new-link'), {
            'title': u'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'language': 'en',
            'level': 'beginner'
        })
        self.assertEqual(resp.status_code, 302)


    def test_new_link_ajax_exists(self):
        self.client.login(username=self.user.username, password='test123')

        alist = ListFactory()
        alist.owner = self.user
        alist.md_content = '#titre'
        alist.save()

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'language': 'en',
            'level': 'beginner',
            'ajax': '1',
            'id': alist.pk,
        })

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'language': 'en',
            'level': 'beginner',
        })
        self.assertEqual(resp.status_code, 302)

    def test_new_link_invalid(self):
        self.client.login(username=self.user.username, password='test123')

        alist = ListFactory()
        alist.owner = self.user
        alist.save()

        resp = self.client.post(reverse('new-link'), {
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
        })

        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse('new-link'), {
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'ajax': '1'
        })

        self.assertEqual(resp.status_code, 200)
