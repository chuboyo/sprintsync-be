from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


# Create your tests here.
class UserAPITest(APITestCase):
    def setUp(self):
        
        self.user = get_user_model().objects.create_user(
             email='chuboyo@gmail.com',
             username='chubiyojo',
             password='password'
        )

    def test_register_user(self):
        """
        Ensure we can register a new user.
        """
        url = reverse('user-list')
        data = {'username': 'fantastic',
                'email': 'fantastic@email.com',
                'password': '2Password',
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_login(self):
        """Ensure user can login with email and password."""
        url = reverse('user-login')
        data = {'username': 'chubiyojo',
                'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
