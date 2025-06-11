import random
from datetime import datetime, timedelta

from rest_framework.test import APIClient, APITestCase


class AccountingFlowTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "password": "TestPass123!",
            "name": "테스트유저",
        }
        self.account_data = {
            "account_number": "1234567890",
            "bank_code": "090",
            "account_type": "CHECKING",
            "balance": 100000,
        }
        self.analysis_data = {
            "about": "TOTAL_SPENDING",
            "type": "MONTHLY",
            "period_start": "2025-06-01",
            "period_end": "2025-06-30",
        }

    def generate_random_transaction(self, account_id):
        methods = ["CARD", "ATM", "TRANSFER", "AUTOMATIC_TRANSFER"]
        types = ["DEPOSIT", "WITHDRAW"]
        descriptions = ["점심", "커피", "급여", "쇼핑", "교통", "이체", "이자"]

        tx_type = random.choice(types)
        amount = random.randint(1000, 50000)
        method = random.choice(methods)
        desc = random.choice(descriptions)
        balance_after = random.randint(0, 200000)
        random_day = random.randint(1, 30)
        tx_date = datetime(2025, 6, random_day)
        return {
            "account": account_id,
            "amount": amount,
            "balance_after": balance_after,
            "description": desc,
            "transaction_type": tx_type,
            "method": method,
            "transaction_at": tx_date.isoformat(),
        }

    def test_full_accounting_flow(self):
        res = self.client.post("/api/user/signup/", self.user_data)
        print("회원가입:", res.status_code)
        self.assertEqual(res.status_code, 201)

        res = self.client.post("/api/user/signup/", self.user_data)
        print("중복 회원가입 차단:", res.status_code)
        self.assertEqual(res.status_code, 400)

        res = self.client.post(
            "/api/user/login/",
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        print("로그인:", res.status_code)
        self.assertEqual(res.status_code, 200)
        access = res.data["access"]
        refresh = res.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        res = self.client.post("/api/user/logout/", {"refresh": refresh})
        print("로그아웃:", res.status_code)
        self.assertEqual(res.status_code, 205)

        res = self.client.post(
            "/api/user/login/",
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        print("재로그인:", res.status_code)
        self.assertEqual(res.status_code, 200)
        access = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        res = self.client.post("/api/accounts/create/", self.account_data)
        print("계좌 생성:", res.status_code)
        self.assertEqual(res.status_code, 201)
        account_id = res.data["id"]

        success_count = 0
        failures = []

        for i in range(100):
            tx = self.generate_random_transaction(account_id)
            res = self.client.post("/api/transaction/create/", tx)
            if res.status_code == 201:
                success_count += 1
            else:
                failures.append((i + 1, res.status_code, res.json()))

        print(f"거래 100개 랜덤 등록 완료: {success_count}/100 성공")
        if failures:
            print("실패 항목:")
            for f in failures:
                print(f"  #{f[0]} → status: {f[1]}, error: {f[2]}")

        # 최소 90개 이상 성공해야 통과
        self.assertGreaterEqual(success_count, 90)

        res = self.client.get(f"/api/transaction/?account={account_id}")
        tx_id = res.data[0]["id"]
        res = self.client.patch(
            f"/api/transaction/{tx_id}/update/", {"description": "수정된 거래"}
        )
        print("거래 수정:", res.status_code)
        self.assertIn(res.status_code, [200, 202])

        res = self.client.post("/api/analysis/run/", self.analysis_data)
        print("분석 요청:", res.status_code)
        self.assertEqual(res.status_code, 201)
