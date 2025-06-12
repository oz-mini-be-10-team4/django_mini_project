from django.conf import settings  # AUTH_USER_MODEL 사용
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{'읽음' if self.is_read else '미읽음'}] {self.user.username} - {self.message}"
