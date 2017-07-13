from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status



class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.normal_user = User.objects.create(first_name="siddu",username="siddu",email="revansbiradar@gmail.com",
            is_active=True,is_staff=False)
        self.normal_user.set_password('password1234')
        self.normal_user.save()
        self.normal_token, created = Token.objects.get_or_create(user=self.normal_user)
        # URL for creating an account.
        self.create_url = reverse('account_create')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }
        response = self.client.post(self.create_url , data, format='json')
        user = User.objects.latest('id')

        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
            'username': 'foo'*30,
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobar'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
                'username': 'siddu',
                'email': 'user@example.com',
                'password': 'testuser'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
            'username': 'testuser2',
            'email': 'revansbiradar@gmail.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
            'username': 'foobarbaz',
            'email':  'testing',
            'passsword': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
                'username' : 'foobar',
                'email': '',
                'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)


class LogInTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'task',
            'password': 'qwerty123456'
        }
        User.objects.create_user(**self.credentials)
        self.normal_user = User.objects.create(first_name="siddu",username="siddu",email="revansbiradar@gmail.com",
            is_active=True,is_staff=False)
        self.normal_user.set_password('password1234')
        self.normal_user.save()
        self.url = reverse('account_login')
        self.normal_token, created = Token.objects.get_or_create(user=self.normal_user)

    def test_login(self):
        # send login data
        response = self.client.post(self.url, self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

    def test_login_invalid_username(self):
        # send login data
        self.credentials = {
            'username': 'task123',
            'password': 'qwerty123456'

        }
        response = self.client.post(self.url, self.credentials, follow=True)
        self.assertTrue(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_password(self):
        # send login data
        self.credentials = {
            'username': 'task',
            'password': 'qwerty'
        }
        response = self.client.post(self.url, self.credentials, follow=True)
        self.assertTrue(response.status_code, status.HTTP_401_UNAUTHORIZED)




