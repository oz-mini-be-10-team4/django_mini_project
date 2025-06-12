import random
from datetime import datetime

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
        # 1단계: 회원가입
        res = self.client.post("/api/user/signup/", self.user_data)
        print("[1단계] 회원가입 시도 → 상태 코드:", res.status_code)
        print(
            "[1단계] 회원가입 성공 여부:", "성공" if res.status_code == 201 else "실패"
        )
        print()

        # 2단계: 중복 회원가입
        res = self.client.post("/api/user/signup/", self.user_data)
        print("[2단계] 중복 회원가입 시도 → 상태 코드:", res.status_code)
        print(
            "[2단계] 중복 차단 확인:",
            "차단됨" if res.status_code == 400 else "차단 실패",
        )
        print()

        # 3단계: 로그인
        res = self.client.post(
            "/api/user/login/",
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        print("[3단계] 로그인 시도 → 상태 코드:", res.status_code)
        print("[3단계] 로그인 성공 여부:", "성공" if res.status_code == 200 else "실패")
        print()
        access = res.data["access"]
        refresh = res.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        # 4단계: 로그아웃
        res = self.client.post("/api/user/logout/", {"refresh": refresh})
        print("[4단계] 로그아웃 요청 → 상태 코드:", res.status_code)
        print(
            "[4단계] 로그아웃 처리 결과:", "성공" if res.status_code == 205 else "실패"
        )
        print()

        # 5단계: 재로그인
        res = self.client.post(
            "/api/user/login/",
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        print("[5단계] 재로그인 시도 → 상태 코드:", res.status_code)
        print(
            "[5단계] 재로그인 성공 여부:", "성공" if res.status_code == 200 else "실패"
        )
        print()
        access = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        # 6단계: 계좌 생성
        res = self.client.post("/api/accounts/create/", self.account_data)
        print("[6단계] 계좌 생성 요청 → 상태 코드:", res.status_code)
        print("[6단계] 계좌 생성 결과:", "성공" if res.status_code == 201 else "실패")
        print()
        account_id = res.data["id"]

        # 7단계: 거래 100개 등록
        success_count = 0
        failures = []

        for i in range(100):
            tx = self.generate_random_transaction(account_id)
            res = self.client.post("/api/transaction/create/", tx)
            if res.status_code == 201:
                success_count += 1
            else:
                failures.append((i + 1, res.status_code, res.json()))

        print(
            f"[7단계] 거래 100건 등록 결과: 성공 {success_count}건 / 실패 {len(failures)}건"
        )
        if failures:
            print("실패한 거래 목록:")
            for f in failures:
                print(f"  - #{f[0]} → 상태: {f[1]}, 에러: {f[2]}")
        print()
        self.assertGreaterEqual(success_count, 90)

        # 8단계: 거래 수정
        res = self.client.get(f"/api/transaction/?account={account_id}")
        tx_id = res.data[0]["id"]
        res = self.client.patch(
            f"/api/transaction/{tx_id}/update/", {"description": "수정된 거래"}
        )
        print("[8단계] 거래 수정 요청 → 상태 코드:", res.status_code)
        print(
            "[8단계] 거래 수정 결과:",
            "성공" if res.status_code in [200, 202] else "실패",
        )
        print()
        self.assertIn(res.status_code, [200, 202])

        # 9단계: 분석 실행
        res = self.client.post("/api/analysis/run/", self.analysis_data)
        print("[9단계] 분석 실행 요청 → 상태 코드:", res.status_code)
        print("[9단계] 분석 실행 결과:", "성공" if res.status_code == 201 else "실패")
        print()
        self.assertEqual(res.status_code, 201)

        # 10단계: 알림 확인
        res = self.client.get("/api/notifications/unread/")
        print("[10단계] 미확인 알림 조회 → 상태 코드:", res.status_code)
        print(f"[10단계] 확인된 미확인 알림 수: {len(res.data)}개")
        print()
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

        # 11단계: 알림 내용 확인
        notification = res.data[0]
        print("[11단계] 첫 알림 메시지 내용 확인:", notification["message"])
        print()
        self.assertIn("그래프", notification["message"])

        # 12단계: 알림 읽음 처리
        notif_id = notification["id"]
        res = self.client.post(f"/api/notifications/{notif_id}/read/")
        print("[12단계] 알림 읽음 처리 요청 → 상태 코드:", res.status_code)
        print(
            "[12단계] 알림 읽음 처리 결과:",
            "성공" if res.status_code == 200 else "실패",
        )
        print()
        self.assertEqual(res.status_code, 200)

        # 13단계: 읽은 알림 재확인
        res = self.client.get("/api/notifications/unread/")
        print("[13단계] 읽음 처리된 알림 재조회 확인")
        print(
            "[13단계] 읽은 알림이 목록에 남아 있는가?:",
            (
                "남아있지 않음 (정상)"
                if all(n["id"] != notif_id for n in res.data)
                else "남아있음 (문제 발생)"
            ),
        )
        print()
        self.assertTrue(all(n["id"] != notif_id for n in res.data))
