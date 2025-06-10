from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions

from .models import Transaction
from .serializers import TransactionSerializer


# 거래 등록
class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# 거래 목록 조회 (필터링 포함)
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["transaction_type", "method"]
    ordering_fields = ["transaction_at", "amount"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # 스웨거 전용
            return Transaction.objects.none()
        return Transaction.objects.filter(account_id__user_id=self.request.user)


# 거래 수정
class TransactionUpdateView(generics.UpdateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # 스웨거 전용
            return Transaction.objects.none()
        return Transaction.objects.filter(account_id__user_id=self.request.user)


# 거래 삭제
class TransactionDeleteView(generics.DestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # 스웨거 전용
            return Transaction.objects.none()
        return Transaction.objects.filter(account_id__user_id=self.request.user)
