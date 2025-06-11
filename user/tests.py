from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITestCase(APITestCase):
    def setUp(self):
        # 테스트에 사용할 URL과 기본 유저 데이터 설정
        self.signup_url = reverse("user:signup")
        self.login_url = reverse("user:login")
        self.token_refresh_url = reverse("user:token_refresh")
        self.me_url = reverse("user:me")
        self.logout_url = reverse("user:logout")
        self.user_data = {
            "email": "test@example.com",
            "name": "테스트유저",
            "password": "testpassword123",
        }
        # 테스트용 유저 생성
        self.user = User.objects.create_user(
            email=self.user_data["email"],
            password=self.user_data["password"],
            name=self.user_data["name"],
        )

    def test_signup(self):
        # 회원가입 API 정상 동작 테스트
        data = {
            "email": "newuser@example.com",
            "name": "새유저",
            "password": "newpassword123",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # 201 응답 확인
        self.assertTrue(
            User.objects.filter(email=data["email"]).exists()
        )  # 유저 생성 확인
        print("test_signup 완료")

    def test_login(self):
        # 로그인 API 정상 동작 테스트
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 응답 확인
        self.assertIn("access", response.data)  # access 토큰 존재 확인
        self.assertIn("refresh", response.data)  # refresh 토큰 존재 확인
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]
        print("test_login 완료")

    def test_token_refresh(self):
        # 토큰 재발급 API 정상 동작 테스트
        login_response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        refresh_token = login_response.data["refresh"]
        response = self.client.post(self.token_refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 응답 확인
        self.assertIn("access", response.data)  # 새 access 토큰 존재 확인
        print("test_token_refresh 완료")

    def test_me(self):
        # 내 정보 조회 API 정상 동작 테스트
        login_response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        access_token = login_response.data["access"]
        # 인증 헤더에 access 토큰 추가
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 응답 확인
        self.assertEqual(
            response.data["email"], self.user_data["email"]
        )  # 이메일 일치 확인
        self.assertEqual(
            response.data["name"], self.user_data["name"]
        )  # 이름 일치 확인
        print("test_me 완료")

    def test_logout(self):
        # 로그아웃 API 정상 동작 테스트
        login_response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        refresh_token = login_response.data["refresh"]
        access_token = login_response.data["access"]
        # 인증 헤더에 access 토큰 추가
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(self.logout_url, {"refresh": refresh_token})
        self.assertEqual(
            response.status_code, status.HTTP_205_RESET_CONTENT
        )  # 205 응답 확인
        print("test_logout 완료")
