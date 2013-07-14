# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.test.client import Client


class PageTests(TestCase):
    def test_url_home(self):
        client = Client()
        self.assertEqual(200, client.get('/').status_code)
