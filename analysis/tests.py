from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from analysis.models import Analysis

User = get_user_model()


class AnalysisListAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword123", name="테스트유저"
        )
        self.client.login(email="test@example.com", password="testpassword123")

        self.list_url = reverse("analysis:list")

        # 인증 토큰 로그인 방식 사용 시:
        response = self.client.post(
            reverse("user:login"),
            {"email": "test@example.com", "password": "testpassword123"},
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Analysis 데이터 생성
        today = timezone.now().date()
        for i in range(3):
            Analysis.objects.create(
                user=self.user,
                about="총 지출",
                type="WEEKLY" if i % 2 == 0 else "MONTHLY",
                period_start=today - timedelta(days=7 * (i + 1)),
                period_end=today - timedelta(days=7 * i),
                description="테스트 분석",
            )

    # 모두
    def test_get_all_analysis(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        print("test_get_all_analysis 완료")

    # 주 단위
    def test_filter_weekly_analysis(self):
        response = self.client.get(self.list_url + "?type=weekly")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        print("test_filter_weekly_analysis 완료")

    # 월 단위
    def test_filter_monthly_analysis(self):
        response = self.client.get(self.list_url + "?type=monthly")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print("test_filter_monthly_analysis 완료")
