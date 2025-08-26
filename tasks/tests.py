from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Task


# Create your tests here.
class UserAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
             email='chuboyo@gmail.com',
             username='chubiyojo',
             password='password'
        )

        self.task = Task.objects.create(
            title='test task',
            description='the very first task',
            user=self.user
        )

    def test_list_tasks(self):
        client = APIClient()
        client.force_authenticate(user=self.user) 
        url = reverse('task-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'test task')
        self.assertEqual(response.data[0]['description'], 'the very first task')

    def test_create_task(self):
        client = APIClient()
        client.force_authenticate(user=self.user) 
        url = reverse('task-list')
        data = {'title': 'second task',
                'description': 'description for the second task'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'second task')
        self.assertEqual(response.data['description'], 'description for the second task')

    def test_retrieve_task(self):
        client = APIClient()
        client.force_authenticate(user=self.user) 
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test task')
        self.assertEqual(response.data['description'], 'the very first task')

    def test_destroy_tasks(self):
        client = APIClient()
        client.force_authenticate(user=self.user) 
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
