from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account

from .models import Transaction

User = get_user_model()


class TransactionAPITestCase(APITestCase):
    def setUp(self):
        # 테스트용 유저 및 계좌 생성
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword123", name="테스트유저"
        )
        self.account = Account.objects.create(
            user=self.user, account_number="1234567890", balance=100000
        )
        # 로그인 및 토큰 발급
        self.login_url = reverse("user:login")
        login_response = self.client.post(
            self.login_url, {"email": "test@example.com", "password": "testpassword123"}
        )
        self.access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # 트랜잭션 관련 URL
        self.list_url = reverse("transaction:list")
        self.create_url = reverse("transaction:create")

    def test_create_transaction(self):
        # 거래 생성 API 정상 동작 테스트
        data = {
            "account": self.account.id,
            "amount": "5000.00",
            "balance_after": "95000.00",
            "description": "테스트 입금",
            "transaction_type": "DEPOSIT",
            "method": "ATM",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # 201 응답 확인
        self.assertTrue(
            Transaction.objects.filter(account=self.account, amount="5000.00").exists()
        )  # 생성 확인
        print("test_create_transaction 완료")

    def test_list_transaction(self):
        # 거래 목록 조회 API 정상 동작 테스트
        Transaction.objects.create(
            account=self.account,
            amount="1000.00",
            balance_after="99000.00",
            description="테스트 출금",
            transaction_type="WITHDRAW",
            method="TRANSFER",
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 응답 확인
        self.assertGreaterEqual(len(response.data), 1)  # 최소 1개 이상 존재
        print("test_list_transaction 완료")

    def test_update_transaction(self):
        # 거래 수정 API 정상 동작 테스트
        transaction = Transaction.objects.create(
            account=self.account,
            amount="2000.00",
            balance_after="98000.00",
            description="수정 전",
            transaction_type="DEPOSIT",
            method="CASH",
        )
        update_url = reverse("transaction:update", args=[transaction.id])
        data = {"description": "수정 후"}
        response = self.client.patch(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 응답 확인
        transaction.refresh_from_db()
        self.assertEqual(transaction.description, "수정 후")  # 수정 내용 확인
        print("test_update_transaction 완료")

    def test_delete_transaction(self):
        # 거래 삭제 API 정상 동작 테스트
        transaction = Transaction.objects.create(
            account=self.account,
            amount="3000.00",
            balance_after="97000.00",
            description="삭제 테스트",
            transaction_type="WITHDRAW",
            method="TRANSFER",
        )
        delete_url = reverse("transaction:delete", args=[transaction.id])
        response = self.client.delete(delete_url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )  # 204 응답 확인
        self.assertFalse(
            Transaction.objects.filter(id=transaction.id).exists()
        )  # 삭제 확인
        print("test_delete_transaction 완료")
