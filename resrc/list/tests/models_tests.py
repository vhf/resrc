from django.test import TestCase

from resrc.list.models import List, ListLinks
from resrc.link.tests.factories import LinkFactory
from resrc.list.tests.factories import ListFactory
from resrc.tag.tests.factories import TagFactory


class ListTestCase(TestCase):

    def test_model(self):
        """test list model exists"""
        alist = ListFactory()
        alist.save()
        self.assertTrue(alist.pk)

    def test_get_absolute_url(self):
        """test list absolute url"""
        alist = ListFactory()
        alist.save()
        self.assertEqual(alist.get_absolute_url(), '/ls/1/my-own-public-list/')

    def test_slug(self):
        """test list slug"""
        alist = ListFactory()
        alist.save()
        self.assertEqual(alist.do_unique_slug(), False)

        self.assertEqual(alist.slug, 'my-own-public-list')

        alist = ListFactory()
        alist.save()
        self.assertEqual(alist.slug, 'my-own-public-list-1')

    def test_get_tags(self):
        """test list tags"""
        alist = ListFactory()
        alist.save()
        self.assertEqual(list(alist.get_tags()), [])

        link = LinkFactory()
        link.save()

        tag = TagFactory()
        tag.save()

        link.tags.add(tag)
        link.save()

        listlink = ListLinks.objects.create(
            alist=alist,
            links=link
        )

        self.assertEqual(list(alist.get_tags()), [(u'Django', u'django', 1)])

    def test_delete_link_from_list(self):
        alist = ListFactory()
        alist.save()

        link = LinkFactory()
        link.save()

        listlink = ListLinks.objects.create(
            alist=alist,
            links=link
        )
        listlink.save()
        self.assertTrue(
            listlink == ListLinks.objects.get(alist=alist, links=link))

        listlink.delete()
        with self.assertRaises(ListLinks.DoesNotExist):
            ListLinks.objects.get(alist=alist, links=link)

    def test_titles_link_in_default(self):
        a_personal_list = ListFactory()
        a_personal_list.save()
        a_default_list = ListFactory()
        a_default_list.title = "Bookmarks"
        a_default_list.save()

        link = LinkFactory()
        link.save()

        listlink = ListLinks.objects.create(
            alist=a_personal_list,
            links=link
        )
        listlink.save()

        listlink = ListLinks.objects.create(
            alist=a_default_list,
            links=link
        )
        listlink.save()

        self.assertEqual(
            list(List.objects.titles_link_in_default(a_personal_list.owner, link.pk)), [a_personal_list.title])

    def test_personal_lists(self):
        a_personal_list = ListFactory()
        a_personal_list.save()
        a_default_list = ListFactory()
        a_default_list.title = "Bookmarks"
        a_default_list.save()

        link = LinkFactory()
        link.save()

        listlink = ListLinks.objects.create(
            alist=a_personal_list,
            links=link
        )
        listlink.save()

        listlink = ListLinks.objects.create(
            alist=a_default_list,
            links=link
        )
        listlink.save()

        self.assertEqual(
            list(List.objects.personal_lists(a_personal_list.owner)), [a_personal_list])

    def test_user_lists(self):
        a_personal_list = ListFactory()
        a_personal_list.save()
        a_default_list = ListFactory()
        a_default_list.title = "Bookmarks"
        a_default_list.save()

        link = LinkFactory()
        link.save()

        listlink = ListLinks.objects.create(
            alist=a_personal_list,
            links=link
        )
        listlink.save()

        listlink = ListLinks.objects.create(
            alist=a_default_list,
            links=link
        )
        listlink.save()

        self.assertEqual(
            list(List.objects.user_lists(a_personal_list.owner, False)), [a_personal_list])

    def test_vote(self):
        """test link comment count"""
        list = ListFactory()
        list.vote()
        list.save()
        self.assertEqual(list.upvotes, 1)
        from datetime import datetime
        hour = datetime.now().hour
        hours = {
            0: 'votes_h00', 1: 'votes_h00', 2: 'votes_h02', 3: 'votes_h02', 4: 'votes_h04',
            5: 'votes_h04', 6: 'votes_h06', 7: 'votes_h06', 8: 'votes_h08', 9: 'votes_h08',
            10: 'votes_h10', 11: 'votes_h10', 12: 'votes_h12', 13: 'votes_h12', 14: 'votes_h14',
            15: 'votes_h14', 16: 'votes_h16', 17: 'votes_h16', 18: 'votes_h18', 19: 'votes_h18',
            20: 'votes_h20', 21: 'votes_h20', 22: 'votes_h22', 23: 'votes_h22'}
        self.assertEqual(getattr(list, hours[hour]), 1)
