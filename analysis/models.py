from django.conf import settings
from django.db import models


class Analysis(models.Model):
    TYPE_CHOICES = (
        ("WEEKLY", "주간"),
        ("MONTHLY", "월간"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.CharField(max_length=100)  # 예: "총 지출"
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    description = models.TextField()
    result_image = models.ImageField(upload_to="analysis/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
