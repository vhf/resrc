# -*- coding: utf-8 -*-:
from django.test import TestCase
from django.core.urlresolvers import reverse

from resrc.userprofile.tests.factories import ProfileFactory, UserFactory
from resrc.language.tests.factories import LanguageFactory
from django.contrib.auth.models import User


class UserprofileViewTestCase(TestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user

        self.profile2 = ProfileFactory()
        self.user2 = self.profile2.user


    def test_user_list(self):
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(resp.status_code, 302)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(resp.status_code, 200)


    def test_my_list_link(self):
        resp = self.client.get(reverse('user-lists', kwargs={
            'user_name': self.user.username
        }))
        self.assertEqual(resp.status_code, 200)


    def test_my_details(self):
        resp = self.client.get(reverse('user-url', kwargs={
            'user_name': self.user.username
        }))
        self.assertEqual(resp.status_code, 200)

        user = UserFactory()
        resp = self.client.get(reverse('user-url', kwargs={
            'user_name': user.username
        }))
        self.assertEqual(resp.status_code, 404)

    def test_login_view(self):
        resp = self.client.post(reverse('user-login'), {
            'username': self.user.username,
            'password': 'test123'
        })
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse('user-login'), {
            'username': self.user.username,
            'password': 'test'
        })
        self.assertEqual(resp.status_code, 200)


        resp = self.client.post(reverse('user-login'), {
            'username': self.user.username,
            'password': 'test123',
            'next': reverse('user-url', kwargs={'user_name': self.user.username})
        })
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post("%s?next=%s" % (
            reverse('user-login-modal'),
            reverse('user-url', kwargs={'user_name': self.user.username})
            ), {
            'username': self.user.username,
            'password': 'test',
            'next': reverse('user-url', kwargs={'user_name': self.user.username})
        })
        self.assertEqual(resp.status_code, 200)


    def test_register_view(self):
        resp = self.client.post(reverse('user-register'), {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'test123',
            'password_confirm': 'test'
        })
        self.assertEqual(resp.status_code, 200)

        from captcha.models import CaptchaStore
        captcha = CaptchaStore.objects.all()[0]


        resp = self.client.post(reverse('user-register'), {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'test123',
            'password_confirm': 'test123',
            'captcha_0': captcha.hashkey,
            'captcha_1': captcha.response
        })
        self.assertEqual(resp.status_code, 302)
        created_user = User.objects.get(username='test')
        self.assertEqual(created_user.email, 'test@example.com')


    def test_register_success(self):
        resp = self.client.get(reverse('user-register-success'))
        self.assertEqual(resp.status_code, 302)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('user-register-success'))
        self.assertEqual(resp.status_code, 200)


    def test_logout(self):
        resp = self.client.get(reverse('user-logout'))
        self.assertEqual(resp.status_code, 302)

        self.client.login(username=self.user.username, password='test123')
        #if logged in
        resp = self.client.get(reverse('user-register-success'))
        self.assertEqual(resp.status_code, 200)

        #then logout, get redirected
        resp = self.client.get(reverse('user-logout'))
        self.assertEqual(resp.status_code, 302)

        #no more access
        resp = self.client.get(reverse('user-register-success'))
        self.assertEqual(resp.status_code, 302)


    def test_settings_profile(self):
        resp = self.client.get(reverse('user-settings'))
        self.assertEqual(resp.status_code, 302)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('user-settings'))
        self.assertEqual(resp.status_code, 200)

        lang = LanguageFactory()
        lang.save()
        from resrc.language.models import Language

        resp = self.client.post(reverse('user-settings'), {
            'about': 'My short bio.',
            'email': self.user.email,
            'languages': Language.objects.get(pk=1).pk,
            'show_email': True
        })
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse('user-settings'), {
            'about': 'My short bio.',
            'email': self.user.email,
            'languages': Language.objects.get(pk=1).pk
        })
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse('user-settings'), {
            'about': 'My short bio.'
        })
        self.assertEqual(resp.status_code, 200)


    def test_settings_account(self):
        resp = self.client.get(reverse('user-account'))
        self.assertEqual(resp.status_code, 302)

        self.client.login(username=self.user.username, password='test123')
        resp = self.client.get(reverse('user-account'))
        self.assertEqual(resp.status_code, 200)

        lang = LanguageFactory()
        lang.save()
        from resrc.language.models import Language

        resp = self.client.post(reverse('user-account'), {
            'password_old': 'test123',
            'password_new': 'test1234',
            'password_confirm': 'test1234'
        })
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse('user-account'), {
            'password_old': 'test1234',
            'password_new': 'test1232',
            'password_confirm': 'test1234'
        })
        self.assertEqual(resp.status_code, 200)
