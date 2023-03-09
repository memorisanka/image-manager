from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient


class MyImageViewsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
