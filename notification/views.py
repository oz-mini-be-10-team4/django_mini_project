from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)


class NotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return Response(
                {"detail": "알림을 읽음 처리했습니다."}, status=status.HTTP_200_OK
            )
        except Notification.DoesNotExist:
            return Response(
                {"detail": "해당 알림이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
