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


class SignInView(TestCase):
    '''This tests to see if the sign in view works.'''
    def test_signin_view(self):
        resp = self.client.get(reverse('accounts:sign_in'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/sign_in.html')
        self.assertContains(resp, 'Username:')
        self.assertContains(resp, 'Password:')


class SignUpView(TestCase):
    '''This tests to see if the sign up view works.'''
    def test_signup_view(self):
        resp = self.client.get(reverse('accounts:sign_up'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/sign_up.html')
        self.assertContains(resp, 'Username:')
        self.assertContains(resp, 'Password:')
        self.assertContains(resp, 'Required. 30 characters or fewer.')
