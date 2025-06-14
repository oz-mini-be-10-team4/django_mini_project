from rest_framework import generics, permissions

from .models import Account
from .serializers import AccountSerializer


# 계좌 등록
class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# 계좌 목록 조회
class AccountListView(generics.ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # Swagger 예외 처리
            return Account.objects.none()
        return Account.objects.filter(user_id=self.request.user)


# 계좌 삭제
class AccountDeleteView(generics.DestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # Swagger 예외 처리
            return Account.objects.none()
        return Account.objects.filter(user_id=self.request.user)
