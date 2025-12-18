from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import usersDetail

class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = usersDetail.objects.create(name='User1', email='user1@example.com')
        self.user2 = usersDetail.objects.create(name='User2', email='user2@example.com')

    def test_fetch_users_api(self):
        url = reverse('fetch_users_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 

    def test_fetch_user_api(self):
        url = reverse('fetch_user_api', kwargs={'pk': self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'User1')

    def test_update_user_api(self):
        url = reverse('update_user_api', kwargs={'pk': self.user1.pk})
        data = {'name': 'Updated User'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, 'Updated User')

    def test_delete_user_api(self):
        url = reverse('delete_user_api', kwargs={'pk': self.user1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(usersDetail.DoesNotExist):
            self.user1.refresh_from_db()

    def test_add_user_api(self):
        url = reverse('add_user_api')
        data = {'name': 'New User', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(usersDetail.objects.filter(name='New User').exists())
