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


    def test_ajax_upvote_link(self):
        link = LinkFactory()
        link.author = self.user
        link.save()
        resp = self.client.get(reverse('link-upvote', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 403)
        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('link-upvote', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 403)
        #vote
        resp = self.client.post(reverse('link-upvote', kwargs={'link_pk': link.pk}), {})
        self.assertEqual(resp.status_code, 200)
        #unvote
        resp = self.client.post(reverse('link-upvote', kwargs={'link_pk': link.pk}), {})
        self.assertEqual(resp.status_code, 200)


    def test_ajax_revise_link(self):
        link = LinkFactory()
        link.author = self.user
        link.save()
        resp = self.client.get(reverse('revise-link', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 403)
        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('revise-link', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 403)

        resp = self.client.post(reverse('revise-link', kwargs={'link_pk': link.pk}), {
            'title': 'example',
            'url': 'http://example.com',
            'language': 'en',
            'level': 'beginner',
            'tags': 'Python'
        })
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse('revise-link', kwargs={'link_pk': link.pk}), {
            'title': link.title,
            'url': link.url,
            'language': 'en',
            'level': 'beginner',
            'tags': 'Python'
        })
        self.assertEqual(resp.status_code, 200)


    def test_edit_link_view(self):
        link = LinkFactory()
        link.author = self.user
        link.save()
        resp = self.client.get(reverse('link-edit', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 302)
        self.client.login(username=self.user2.username, password='test123')
        resp = self.client.get(reverse('link-edit', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 404)
        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('link-edit', kwargs={'link_pk': link.pk}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse('link-edit', kwargs={'link_pk': link.pk}), {
            'title': u'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': 'Ruby, "Static Site Generator", "Ruby on Rails"',
            'language': 'en',
            'level': 'beginner'
        })
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse('link-edit', kwargs={'link_pk': link.pk}), {
            'title': u'Building static websites with Middleman, deploying to Heroku',
            'url': 'http://12devs.co.uk/articles/204/',
            'tags': '"Static Site Generator", "Ruby on Rails"',
            'language': 'en',
            'level': 'beginner'
        })
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse('link-edit', kwargs={'link_pk': link.pk}), {
            'title': u'Building static websites with Middleman, deploying to Heroku',
        })
        self.assertEqual(resp.status_code, 200)


    def test_links_page(self):
        resp = self.client.get(reverse('links'))
        self.assertEqual(resp.status_code, 200)
        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('links'))
        self.assertEqual(resp.status_code, 200)


    def test_my_links(self):
        resp = self.client.get(reverse('my-links'))
        self.assertEqual(resp.status_code, 302)
        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('my-links'))
        self.assertEqual(resp.status_code, 200)


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


        resp = self.client.get(reverse('new-link'))
        self.assertEqual(resp.status_code, 200)


    def test_new_link_params_view(self):
        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(
            reverse('new-link-popup', kwargs={'title': 'example', 'url': 'http://example.com'}))
        self.assertEqual(resp.status_code, 200)


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


    def test_single_view(self):
        resp = self.client.get(reverse('link-single-slug', kwargs={
            'link_pk': 1,
            'link_slug': 'something'
        }))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(reverse('link-single', kwargs={
            'link_pk': 1
        }))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse('link-single-slug', kwargs={
            'link_pk': 1,
            'link_slug': 'building-static-websites-with-middleman-deploying-to-heroku'
        }))
        self.assertEqual(resp.status_code, 200)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('link-single-slug', kwargs={
            'link_pk': 1,
            'link_slug': 'building-static-websites-with-middleman-deploying-to-heroku'
        }))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('link-single', kwargs={
            'link_pk': 1
        }))
        # if no slug, redirect to URL with slug
        self.assertEqual(resp.status_code, 302)


    def test_upvoted_list(self):
        resp = self.client.get(reverse('upvoted-list'))
        self.assertEqual(resp.status_code, 302)
        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('upvoted-list'))
        self.assertEqual(resp.status_code, 200)
