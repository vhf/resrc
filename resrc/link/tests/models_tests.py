from django.test import TestCase
from resrc.userprofile.tests.factories import UserFactory, ProfileFactory

from resrc.link.tests.factories import LinkFactory
from resrc.list.tests.factories import ListFactory

from resrc.link.models import Link


class UserprofileTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user

        self.profile2 = ProfileFactory()
        self.user2 = self.profile2.user

    def test_latest(self):
        link = LinkFactory()
        link.author = self.user
        link.title = 'A'
        link.save()
        link2 = LinkFactory()
        link.title = 'B'
        link2.author = self.user
        link2.save()

        self.assertEqual(Link.objects.latest(1, [1])[0]['title'],
            Link.objects.all()[0].title)

    def test_slug(self):
        """test link slug"""
        link = LinkFactory()
        link.author = self.user
        link.save()
        self.assertEqual(link.do_unique_slug(), False)
        self.assertEqual(
            link.slug, 'example-8')

        link = LinkFactory()
        link.author = self.user
        link.save()
        self.assertEqual(
            link.slug, 'example-9')

    def test_lang(self):
        link = LinkFactory()
        link.author = self.user
        self.assertEqual(link.get_lang(), 'English')

    def test_get_votes(self):
        user = UserFactory()
        user.save()
        profile = ProfileFactory()
        profile.user = user
        profile.save()
        link = LinkFactory()
        link.author_id = user.pk
        self.assertEqual(link.get_votes(), 0)

    def test_categories(self):
        link = LinkFactory()
        link.author = self.user
        link.save()
        self.assertEqual(link.get_categories(), "")

        link.tags.add('book')
        link.tags.add('article')
        link.tags.add('something')
        self.assertEqual(link.get_categories(), "(book/article)")

    def test_vote(self):
        link = LinkFactory()
        link.author = self.user
        link.save()
        alist = ListFactory()
        alist.save()
        link.vote(self.user, alist.pk)

        link = LinkFactory()
        link.author = self.user2
        link.save()
        link.vote(self.user)

        link.unvote(self.user)
        self.assertEqual(self.profile.karma, 0)
        self.assertEqual(self.profile2.karma, 0)
