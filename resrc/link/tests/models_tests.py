from django.test import TestCase

from resrc.link.tests.factories import LinkFactory


class LinkTestCase(TestCase):

    def test_model(self):
        """test link model exists"""
        link = LinkFactory()
        link.save()
        self.assertTrue(link.pk)

    def test_get_absolute_url(self):
        """test link absolute url"""
        link = LinkFactory()
        link.save()
        self.assertEqual(link.get_absolute_url(), '/lk/1/single-page-simple-comprehensive-overview-of-javascript/')

    def test_slug(self):
        """test link slug"""
        link = LinkFactory()
        link.save()
        self.assertEqual(link.do_unique_slug(), False)
        self.assertEqual(link.slug, 'single-page-simple-comprehensive-overview-of-javascript')

        link = LinkFactory()
        link.save()
        self.assertEqual(link.slug, 'single-page-simple-comprehensive-overview-of-javascript-1')

    def test_get_comment_count(self):
        """test link comment count"""
        link = LinkFactory()
        link.save()
        self.assertEqual(link.get_comment_count(), 0)
        #new comment, then assert 1
