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
        self.assertEqual(
            link.get_absolute_url(), '/lk/1/single-page-simple-comprehensive-overview-of-javascript/')

    def test_hash(self):
        """test link hash"""
        link = LinkFactory()
        link.save()
        self.assertEqual(link.hash2, '2i1kc0y52iw')

    def test_slug(self):
        """test link slug"""
        link = LinkFactory()
        link.save()
        self.assertEqual(link.do_unique_slug(), False)
        self.assertEqual(
            link.slug, 'single-page-simple-comprehensive-overview-of-javascript')

        link = LinkFactory()
        link.save()
        self.assertEqual(
            link.slug, 'single-page-simple-comprehensive-overview-of-javascript-1')

    def test_get_comment_count(self):
        """test link comment count"""
        link = LinkFactory()
        link.save()
        self.assertEqual(link.get_comment_count(), 0)
        # new comment, then assert 1

    def test_vote(self):
        """test link comment count"""
        link = LinkFactory()
        link.vote()
        link.save()
        self.assertEqual(link.upvotes, 1)
        from datetime import datetime
        hour = datetime.now().hour
        hours = {
            0: 'votes_h00', 1: 'votes_h00', 2: 'votes_h02', 3: 'votes_h02', 4: 'votes_h04',
            5: 'votes_h04', 6: 'votes_h06', 7: 'votes_h06', 8: 'votes_h08', 9: 'votes_h08',
            10: 'votes_h10', 11: 'votes_h10', 12: 'votes_h12', 13: 'votes_h12', 14: 'votes_h14',
            15: 'votes_h14', 16: 'votes_h16', 17: 'votes_h16', 18: 'votes_h18', 19: 'votes_h18',
            20: 'votes_h20', 21: 'votes_h20', 22: 'votes_h22', 23: 'votes_h22'}
        self.assertEqual(getattr(link, hours[hour]), 1)
