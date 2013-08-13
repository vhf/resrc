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

        self.assertEqual(list(alist.get_tags()), [(u'Django', 1)])

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
