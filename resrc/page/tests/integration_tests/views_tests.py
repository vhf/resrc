# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse


class PageTests(TestCase):

    def test_url_home(self):
        resp = self.client.get(reverse('page-home'))
        self.assertEqual(resp.status_code, 200)

    def test_url_about(self):
        resp = self.client.get(reverse('page-about'))
        self.assertEqual(resp.status_code, 200)

    def test_url_faq(self):
        resp = self.client.get(reverse('page-faq'))
        self.assertEqual(resp.status_code, 200)


class HomeViewTestCase(TestCase):

    """Tests for the ``HomeView`` generic view class."""

    def get_view_name(self):
        """
        I would advise to always define this method.

        As your view grows you will add many more tests which will all call
        ``self.client.get(reverse('name_of_your_view'))``. If you ever decide
        to change that name in your ``urls.py`` you would only have to change
        this string at this central position.

        And trust me: You _will_ change your view name after a while ;)

        """
        return 'page-home'

    def test_view(self):
        resp = self.client.get(reverse(self.get_view_name()))
        self.assertEqual(resp.status_code, 200)
