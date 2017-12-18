import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Profile


class ProfileModelTest(TestCase):
    '''This tests to see if the Profile model works.'''
    def setUp(self):
        # This creates a User model to attach the Profile model to.
        self.user = User.objects.create_user(
            username='tester',
            email='test@test.com',
            password='verysecret1'
        )

    def test_profile_creation(self):
        '''This tests to see if the Profile model works.'''
        profile = Profile.objects.create(
            user=self.user,
            first_name='first',
            last_name='last',
            email='testemail@test.com',
            date_of_birth=datetime.datetime.now().date(),
            bio='I provide safety and security to this applicaion.',
            # leaving avatar blank
            hobby='Helping people create profiles.',
            country='United States of America'
        )
        self.assertEqual(profile.first_name, 'first')
        self.assertEqual(profile.country, 'United States of America')
        self.assertEqual(profile.date_of_birth, datetime.datetime.now().date())


class SignUpView(TestCase):
    '''This tests to see if the sign up view works.'''
    def test_signup_view(self):
        resp = self.client.get(reverse('accounts:sign_up'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/sign_up.html')
        self.assertContains(resp, 'Username:')
        self.assertContains(resp, 'Password:')
        self.assertContains(resp, 'Required. 30 characters or fewer.')


class SignInView(TestCase):
    '''This tests to see if the sign in view works.'''
    def test_signin_view(self):
        resp = self.client.get(reverse('accounts:sign_in'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/sign_in.html')
        self.assertContains(resp, 'Username:')
        self.assertContains(resp, 'Password:')


class LogoutURL(TestCase):
    '''This tests to see if the user has been logged out.'''
    def test_logout_url(self):
        # logs the user in
        self.client.force_login(User.objects.get_or_create(username='test')[0])
        # 'accounts:sign_out' logs the user out.
        self.client.get(reverse('accounts:sign_out'))
        self.assertNotIn('_auth_user_id', self.client.session)


class ProfileView(TestCase):
    '''This tests to see if the profile view works.'''
    def setUp(self):
        # This creates a User model to attach the Profile model to.
        self.user = User.objects.create_user(
            username='tester',
            email='test@test.com',
            password='verysecret1'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            first_name='first',
            last_name='last',
            email='testemail@test.com',
            date_of_birth=datetime.datetime.now().date(),
            bio='I provide safety and security to this applicaion.',
            # leaving avatar blank
            hobby='Helping people create profiles.',
            country='United States of America'
        )

    def test_profile_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('accounts:profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/profile_view.html')
        self.assertContains(resp, 'first')
        self.assertContains(resp, 'I provide safety')
        self.assertContains(resp, 'United States')
