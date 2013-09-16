# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate

from resrc.link.tests.factories import LinkFactory
from resrc.tests.factories import UserFactory
from resrc.tag.tests.factories import TagFactory
from resrc.list.tests.factories import ListFactory
from resrc.link.models import Link
from resrc.list.models import List


class LinkViewTestCase(TestCase):

    def test_single_view(self):
        link = LinkFactory()
        link.save()
        resp = self.client.get(
            reverse('link-single', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse('link-single', kwargs={'link_pk': 77}))
        self.assertEqual(resp.status_code, 404)

    def test_single_slug_view(self):
        link = LinkFactory()
        link.save()
        resp = self.client.get(
            reverse('link-single-slug', kwargs={'link_pk': link.pk, 'link_slug': link.slug}))
        self.assertEqual(resp.status_code, 200)

        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')
        resp = self.client.get(
            reverse('link-single-slug', kwargs={'link_pk': link.pk, 'link_slug': link.slug}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            reverse('link-single-slug', kwargs={'link_pk': link.pk, 'link_slug': link.slug + "x"}))
        self.assertEqual(resp.status_code, 404)

    def test_new_link_view(self):
        resp = self.client.get(reverse('new-link'))
        self.assertEqual(resp.status_code, 302)

        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')
        resp = self.client.get(reverse('new-link'))
        self.assertEqual(resp.status_code, 200)

    def test_new_link_post_view(self):
        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"'
        })
        link = Link.objects.get(url="http://12devs.co.uk/articles/204/")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            link.title, 'Building static websites with Middleman, deploying to Heroku')

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"'
        })
        self.assertEqual(resp.status_code, 302)

    def test_new_link_ajax_view(self):
        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'ajax': '1',
            'id': 91329123,
        })
        self.assertEqual(resp.status_code, 404)

        alist = ListFactory()
        alist.owner = user
        alist.save()
        alist = List.objects.get(owner=user)
        link = Link.objects.get(url="http://12devs.co.uk/articles/204/")

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
        })
        self.assertEqual(resp.status_code, 302)

    def test_new_link_ajax_notmylist(self):
        user = UserFactory()
        user.username = 'hehe'
        user.save()
        user2 = UserFactory()
        user2.username = 'haha'
        user2.save()
        self.client.login(username=user.username, password='test123')

        alist = ListFactory()
        alist.owner = user2
        alist.save()

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'ajax': '1',
            'id': alist.pk,
        })

        self.assertEqual(resp.status_code, 404)

    def test_new_link_ajax_exists(self):
        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')

        alist = ListFactory()
        alist.owner = user
        alist.md_content = '#titre'
        alist.save()

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'ajax': '1',
            'id': alist.pk,
        })

        resp = self.client.post(reverse('new-link'), {
            'title': 'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
        })
        self.assertEqual(resp.status_code, 302)

    def test_new_link_invalid(self):
        user = UserFactory()
        user.save()
        self.client.login(username=user.username, password='test123')

        alist = ListFactory()
        alist.owner = user
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
