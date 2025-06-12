from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Notification

User = get_user_model()


class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="1234")
        self.client = APIClient()
        self.client.login(username="testuser", password="1234")
        Notification.objects.create(user=self.user, message="테스트 알림")

    def test_unread_notifications(self):
        response = self.client.get("/notifications/unread/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_read_notification(self):
        notif = Notification.objects.first()
        response = self.client.post(f"/notifications/{notif.pk}/read/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
