from django.test import TestCase
from resrc.userprofile.tests.factories import UserFactory, ProfileFactory
from resrc.link.tests.factories import LinkFactory
from resrc.list.tests.factories import ListFactory
from resrc.list.models import List, ListLinks

class UserprofileTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user
        self.list = ListFactory()
        self.link = LinkFactory()


    def model_test(self):
        self.list.save()
        self.assertTrue(self.list.pk)

        self.list.delete()
        self.assertEqual(self.list.pk, None)


    def test_lists(self):
        readinglist = ListFactory()
        readinglist.title = "Reading list"
        readinglist.owner = self.user
        readinglist.save()

        alist = ListFactory()
        alist.owner = self.user
        alist.save()

        link = LinkFactory()
        link.author = self.user
        link.save()
        listlink = ListLinks.objects.create(
            alist=alist,
            links=link
        )
        listlink.add()

        self.assertEqual(List.objects.personal_lists(self.user)[0], alist)
        self.assertEqual(List.objects.my_list_titles(self.user, link.pk)[0], alist)


    def test_latest(self):
        import datetime

        alist2 = ListFactory()
        alist2.title = "Latest"
        alist2.owner = self.user
        alist2.pubdate = datetime.date.today()
        alist2.save()

        alist = ListFactory()
        alist.title = "Not the latest"
        alist.owner = self.user
        alist.pubdate = datetime.date.today()-datetime.timedelta(10)
        alist.save()

        self.assertEqual(List.objects.latest(limit=1)[0], alist2)


    def test_most_viewed(self):
        alist = ListFactory()
        alist.title = "Most viewed"
        alist.owner = self.user
        alist.views = 100
        alist.save()

        alist2 = ListFactory()
        alist2.title = "Not the most viewed"
        alist2.owner = self.user
        alist2.views = 10
        alist2.save()
        self.assertEqual(List.objects.most_viewed(limit=1)[0], alist)


    def test_slug(self):
        alist = ListFactory()
        alist.owner = self.user
        alist.save()

        alist2 = ListFactory()
        alist2.owner = self.user
        alist2.save()

        self.assertEqual(alist.slug, 'my-own-public-list')
        self.assertEqual(alist2.slug, 'my-own-public-list-1')


    def test_get_tags(self):
        alist = ListFactory()
        alist.owner = self.user
        alist.save()

        link = LinkFactory()
        link.author = self.user
        link.save()
        self.assertEqual(link.get_categories(), "")

        link.tags.add('book')
        link.tags.add('article')
        link.tags.add('something')

        listlink = ListLinks.objects.create(
            alist=alist,
            links=link
        )
        listlink.add()

        self.assertEqual(alist.get_tags()[0], (u'article', u'article', 1))
        self.assertEqual(alist.get_tags()[1], (u'book', u'book', 1))
        self.assertEqual(alist.get_tags()[2], (u'something', u'something', 1))

        listlink.remove()


    def test_votes(self):
        profile2 = ProfileFactory()
        user2 = profile2.user

        alist = ListFactory()
        alist.owner = user2
        alist.save()

        self.assertEqual(alist.get_votes(), 0)

        alist.vote(self.user)

        self.assertEqual(alist.get_votes(), 1)

        alist.unvote(self.user)

        self.assertEqual(alist.get_votes(), 0)
