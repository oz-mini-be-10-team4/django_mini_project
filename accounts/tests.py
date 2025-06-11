from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Account

User = get_user_model()


class AccountAPITestCase(APITestCase):
    def setUp(self):
        # 테스트용 유저 생성 및 로그인
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword123", name="테스트유저"
        )
        self.login_url = reverse("user:login")
        login_response = self.client.post(
            self.login_url, {"email": "test@example.com", "password": "testpassword123"}
        )
        self.access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # 계좌 관련 URL
        self.list_url = reverse("accounts:list")
        self.create_url = reverse("accounts:create")

    def test_create_account(self):
        # 계좌 생성 API 정상 동작 테스트
        data = {
            "account_number": "1234567890",
            "bank_code": "001",  # 실제 BANK_CODES에 맞게 입력
            "account_type": "SAVING",  # 실제 ACCOUNT_TYPE에 맞게 입력
            "balance": "100000.00",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # 201 응답 확인
        self.assertTrue(
            Account.objects.filter(account_number="1234567890").exists()
        )  # 생성 확인
        print("test_create_account 완료")

    def test_list_account(self):
        # 계좌 목록 조회 API 정상 동작 테스트
        Account.objects.create(
            user=self.user,
            account_number="1111222233",
            bank_code="001",
            account_type="SAVINGS",
            balance="50000.00",
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 응답 확인
        self.assertGreaterEqual(len(response.data), 1)  # 최소 1개 이상 존재
        print("test_list_account 완료")

    def test_delete_account(self):
        # 계좌 삭제 API 정상 동작 테스트
        account = Account.objects.create(
            user=self.user,
            account_number="2222333344",
            bank_code="001",
            account_type="SAVINGS",
            balance="30000.00",
        )
        delete_url = reverse("accounts:delete", args=[account.id])
        response = self.client.delete(delete_url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )  # 204 응답 확인
        self.assertFalse(Account.objects.filter(id=account.id).exists())  # 삭제 확인
        print("test_delete_account 완료")
